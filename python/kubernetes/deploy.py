#!/usr/bin/env python3

# Author: Stephen Cole
# Version: 1.1
# Changes: 2025-03-28 - Added docstrings, fixed typos, and added variable to capture script name for usage info
# 
# Script to create/delete/verify Kubernetes deployments.
# Change the variable DEFAULT_FILE_PATTERN as needed.

import glob
import argparse
import yaml
import sys

from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

# Change this variable to update the default file pattern for YAML files.

DEFAULT_FILE_PATTERN = "*.yaml"

def create_deployments(file_pattern):
    """
    Create Kubernetes resources defined in YAML files matching the given file pattern.

    Parameters:
        file_pattern (str): Glob pattern to match YAML files.
    """
    k8s_client = client.ApiClient()
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files matching pattern '{file_pattern}' found.")
        return
    for filename in files:
        print(f"Creating deployment from: {filename}")
        try:
            utils.create_from_yaml(k8s_client, filename)
        except ApiException as e:
            # If the resource already exists, skip it.
            if e.status == 409 and "already exists" in e.body:
                print(f"Resource in {filename} already exists, skipping.")
            else:
                print(f"Error creating deployment from {filename}: {e}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Resource in {filename} already exists, skipping.")
            else:
                print(f"Error creating deployment from {filename}: {e}")

def delete_deployments(file_pattern):
    """
    Delete Kubernetes resources defined in YAML files matching the file pattern.

    Parameters:
        file_pattern (str): Glob pattern to match YAML files.
    """
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files matching pattern '{file_pattern}' found.")
        return
    for filename in files:
        print(f"Stopping deployment from: {filename}")
        with open(filename, 'r') as f:
            docs = list(yaml.safe_load_all(f))
        for doc in docs:
            if not doc:
                continue
            kind = doc.get("kind")
            metadata = doc.get("metadata", {})
            name = metadata.get("name")
            # For Namespace resources, there's no 'namespace' field.
            namespace = metadata.get("namespace", "default") if kind != "Namespace" else None

            if not name:
                print(f"Skipping {filename} because no name is defined in metadata")
                continue

            try:
                if kind == "Deployment":
                    apps_v1 = client.AppsV1Api()
                    apps_v1.delete_namespaced_deployment(
                        name=name,
                        namespace=namespace,
                        body=client.V1DeleteOptions()
                    )
                    print(f"Deleted Deployment: {name} in namespace {namespace}")
                elif kind == "Service":
                    core_v1 = client.CoreV1Api()
                    core_v1.delete_namespaced_service(
                        name=name,
                        namespace=namespace,
                        body=client.V1DeleteOptions()
                    )
                    print(f"Deleted Service: {name} in namespace {namespace}")
                elif kind == "Pod":
                    core_v1 = client.CoreV1Api()
                    core_v1.delete_namespaced_pod(
                        name=name,
                        namespace=namespace,
                        body=client.V1DeleteOptions()
                    )
                    print(f"Deleted Pod: {name} in namespace {namespace}")
                elif kind == "Namespace":
                    core_v1 = client.CoreV1Api()
                    core_v1.delete_namespace(
                        name=name,
                        body=client.V1DeleteOptions()
                    )
                    print(f"Deleted Namespace: {name}")
                else:
                    print(f"Resource kind '{kind}' in {filename} is not handled by this script.")
            except ApiException as e:
                if e.status == 404:
                    print(f"{kind} {name} not found; it may have already been deleted.")
                else:
                    ns_info = f"in namespace {namespace}" if namespace else ""
                    print(f"Error deleting {kind} {name} {ns_info} from {filename}: {e}")
            except Exception as e:
                ns_info = f"in namespace {namespace}" if namespace else ""
                print(f"Error deleting {kind} {name} {ns_info} from {filename}: {e}")

def display_all_pods():
    """
    Display all pods across all namespaces, similar to 'kubectl get pods -A'.
    """
    print("\nListing all pods across all namespaces:\n")
    core_v1 = client.CoreV1Api()
    pods = core_v1.list_pod_for_all_namespaces(watch=False)
    header = "{:<20} {:<50} {:<10} {:<10} {:<10}"
    print(header.format("NAMESPACE", "NAME", "READY", "STATUS", "RESTARTS"))
    for pod in pods.items:
        namespace = pod.metadata.namespace
        name = pod.metadata.name
        if pod.status.container_statuses:
            ready_count = sum(1 for cs in pod.status.container_statuses if cs.ready)
            total = len(pod.status.container_statuses)
            ready_str = f"{ready_count}/{total}"
            restarts = sum(cs.restart_count for cs in pod.status.container_statuses)
        else:
            ready_str = "0/0"
            restarts = 0
        status = pod.status.phase
        print(header.format(namespace, name, ready_str, status, restarts))

def main():
    """
    Main entry point for the script.
    Loads Kubernetes configuration, parses command-line arguments, and displays
    pod status or creates/deletes deployments based on provided arguments.
    """
    # Load Kubernetes configuration (defaults to ~/.kube/config)
    config.load_kube_config()
    parser = argparse.ArgumentParser(
        description="Create (start) and delete (stop) Kubernetes resources from YAML files."
    )
    # Make 'action' an optional positional argument.
    parser.add_argument(
        "action",
        nargs="?",
        choices=["create", "delete"],
        help="Action to perform: 'create' to start deployments, 'delete' to stop them."
    )
    parser.add_argument(
        "--pattern",
        default=DEFAULT_FILE_PATTERN,
        help=f"File pattern for the YAML files (default: '{DEFAULT_FILE_PATTERN}')."
    )
    args = parser.parse_args()

    # If no action is provided, display pods and usage instructions.
    if args.action is None:
        display_all_pods()
        script_name = sys.argv[0]
        print("\nNo action specified.")
        print("Usage:")
        print(f"  {script_name} create  - Deploy resources from YAML files")
        print(f"  {script_name} delete   - Delete resources defined in YAML files")
        return

    if args.action == "create":
        create_deployments(args.pattern)
    elif args.action == "delete":
        delete_deployments(args.pattern)

    display_all_pods()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3

# Python script to start/stop all Kubernetes deployments/jobs
# in a directory.
#
# Usage:
#
# deploy.py start # Does the equivalent of kubectl apply -f *.yaml
# deploy.py stop # Does the equivalent of kubectl delete -f *.yaml

import glob
import argparse
import yaml
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

DEFAULT_FILE_PATTERN = "*.yaml"

def start_deployments(file_pattern):
    """Create resources defined in YAML files matching the file pattern."""
    k8s_client = client.ApiClient()
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files matching pattern '{file_pattern}' found.")
        return
    for filename in files:
        print(f"Starting deployment from: {filename}")
        try:
            utils.create_from_yaml(k8s_client, filename)
        except ApiException as e:
            # If the resource already exists, skip it.
            if e.status == 409 and "already exists" in e.body:
                print(f"Resource in {filename} already exists, skipping.")
            else:
                print(f"Error starting deployment from {filename}: {e}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Resource in {filename} already exists, skipping.")
            else:
                print(f"Error starting deployment from {filename}: {e}")

def stop_deployments(file_pattern):
    """Delete resources defined in YAML files matching the file pattern."""
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
    """Display all pods across all namespaces (similar to 'kubectl get pods -A')."""
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
    # Load Kubernetes configuration (defaults to ~/.kube/config)
    config.load_kube_config()
    parser = argparse.ArgumentParser(
        description="Demonstration script to create (start) and delete (stop) Kubernetes resources from YAML files."
    )
    parser.add_argument(
        "action",
        choices=["start", "stop"],
        help="Action to perform: 'start' to deploy resources, 'stop' to delete them."
    )
    parser.add_argument(
        "--pattern",
        default="*.yaml",
        help="File pattern for the YAML files (default: '*.yaml')."
    )
    args = parser.parse_args()

    if args.action == "start":
        start_deployments(args.pattern)
    elif args.action == "stop":
        stop_deployments(args.pattern)

    display_all_pods()

if __name__ == '__main__':
    main()strat
import glob
import argparse
import yaml
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException

def start_deployments(file_pattern):
    """Create resources defined in YAML files matching the file pattern."""
    k8s_client = client.ApiClient()
    files = glob.glob(file_pattern)
    if not files:
        print(f"No files matching pattern '{file_pattern}' found.")
        return
    for filename in files:
        print(f"Starting deployment from: {filename}")
        try:
            utils.create_from_yaml(k8s_client, filename)
        except ApiException as e:
            # If the resource already exists, skip it.
            if e.status == 409 and "already exists" in e.body:
                print(f"Resource in {filename} already exists, skipping.")
            else:
                print(f"Error starting deployment from {filename}: {e}")
        except Exception as e:
            if "already exists" in str(e):
                print(f"Resource in {filename} already exists, skipping.")
            else:
                print(f"Error starting deployment from {filename}: {e}")

def stop_deployments(file_pattern):
    """Delete resources defined in YAML files matching the file pattern."""
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
    """Display all pods across all namespaces (similar to 'kubectl get pods -A')."""
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
    # Load Kubernetes configuration (defaults to ~/.kube/config)
    config.load_kube_config()
    parser = argparse.ArgumentParser(
        description="Demonstration script to create (start) and delete (stop) Kubernetes resources from YAML files."
    )
    parser.add_argument(
        "action",
        choices=["start", "stop"],
        help="Action to perform: 'start' to deploy resources, 'stop' to delete them."
    )
    parser.add_argument(
        "--pattern",
        default=DEFAULT_FILE_PATTERN,
        help=f"File pattern for the YAML files (default: '{DEFAULT_FILE_PATTERN}')."
    )
    args = parser.parse_args()

    if args.action == "start":
        start_deployments(args.pattern)
    elif args.action == "stop":
        stop_deployments(args.pattern)

    display_all_pods()

if __name__ == '__main__':
    main()

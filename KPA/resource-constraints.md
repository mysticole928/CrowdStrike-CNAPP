# Adding Resource Contraints to the KPAgent

Kubernetes resource constraints manage how much CPU and memory (RAM) each pod in a cluster can use. 

The contraints are managed through resource requests and resource limits specified in a pod's or container's configuration file.  These are usually found in the `spec.containers section` of a pod's YAML file.

## Resource Requests

- The minimum amount of CPU or memory a container is guaranteed.
- When scheduling a pod, Kubernetes uses the requests to determine which node has enough capacity to run the container.
- The pod is guaranteed at least this amount of resources, even if the node becomes resource-constrained.

## Resource Limits

- The maximum amount of CPU or memory a container is allowed to use.
- When a container tries to exceed the limit, Kubernetes may either throttle (for CPU) or terminate the container (for memory).
- It helps to prevent a container from hogging resources and affecting other containers.

## Add resource contraints to the KPAgent

Create a `json` file with the constraint information and call it something like `kpa-add-contraints.json`

```json
[
  {
    "op": "add",
    "path": "/spec/template/spec/containers/0/resources",
    "value": {
      "limits": {
        "cpu": "250m",
        "memory": "1Gi"
      },
      "requests": {
        "cpu": "250m",
        "memory": "1Gi"
      }
    }
  }
]
```

Use this file with the `kubectl patch` command to update the KPAgent.

```shell
kubectl patch deployment -n falcon-kubernetes-protection \
  kpagent-cs-k8s-protection-agent \
  --type=json \
  --patch-file=kpa-add-contraints.json
```

## Remove contraints from the KPAgent

To remove the contraints from the KPAgent, use `kubectl patch` with a `json` file without the limits. 

Save this `json` as `kpa-remove-constraints.json`:

```json
[
  {
    "op": "remove",
    "path": "/spec/template/spec/containers/0/resources"
  }
]
```

Then, use the file with `kubectl patch` to remove the contraints.

```shell
kubectl patch deployment -n falcon-kubernetes-protection \
  kpagent-cs-k8s-protection-agent \
  --type=json \
  --patch-file=kpa-remove-contraints.json
```

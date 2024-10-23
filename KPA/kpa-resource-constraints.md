# Kubernetes Memory Consumption

The Kubernetes Protection Agent (KPA) memory consumption is directly 
proportional to the number of resources running on the cluster at startup. 

At startup, the KPA waits for the cluster to be in a steady state and then caches the 
state of the cluster. 

The KPA consumes approximately 1GB of memory for every 800-1000 resources on a cluster.

Use this information to se resource constraints to fit the number of resources running on 
a cluster.

## Add Resource Constraints

To add constraints to the KPA use this command:

```bash
kubectl patch deployment -n falcon-kubernetes-protection kpagent-cs-k8s-protection-agent \
  --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/resources", "value":{"limits":{"cpu":"250m","memory":"1Gi"},"requests":{"cpu":"250m","memory":"1Gi"}}}]'
```

Alternatively, here is the `json` that can be saved as a file.

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

Save it with a name like `kpa-patch.json`

To patch the KPA, with the `json` file:

```bash
kubectl patch deployment -n falcon-kubernetes-protection kpagent-cs-k8s-protection-agent \
  --type=json \
  --patch-file=kpa-patch.json
```

## Remove Resource Contraints

To remove the constraints, use this command:

```bash
kubectl patch deployment -n falcon-kubernetes-protection kpagent-cs-k8s-protection-agent --type=json \
--patch='[{"op": "remove", "path": "/spec/template/spec/containers/0/resources" }]'
```

Here's `json` from the above command that can be saved as a file.

```json
[
  {
    "op": "remove",
    "path": "/spec/template/spec/containers/0/resources"
  }
]
```

Save with with a filename like `kpa-remove-contraints.json`.

To remove the resource contraints using that file:

```bash
kubectl patch deployment -n falcon-kubernetes-protection kpagent-cs-k8s-protection-agent \
  --type=json \
  --patch-file=kpa-remove-contraints.json
```




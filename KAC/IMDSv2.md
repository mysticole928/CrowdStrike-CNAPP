# IMDSv2 and the Falcon KAC

Updated: 2024-10-22

In AWS, IMDSv2 encrpyts the metadata tags.  Amazon Linux 2023 has IMDSv2 on by default.  Because of this, EKS cluster names unavailable to the KAC.

It is possible to manually add a cluster name to the KAC.  There are two steps.

## Update the config map

Add the cluster name to the `falcon-kac-meta` config map.

```
kubectl -n falcon-kac patch configmap/falcon-kac-meta \
  --type merge \
  -p '{"data":{"ClusterName":"<---Cluster Name Goes Here--->"}}'
```

## Restart the KAC Pod

The easist way to restart the pod is to delete it.  Kubernetes will automatically replace it.

```
kubectl -n falcon-kac delete pod -l app=falcon-kac
```

## Verify the KAC is Running

### Using `kubectl`

```
kubectl get all -n falcon-kac
```

### Verify the KAC Version using `kubectl`

```
kubectl get pods -n falcon-kac \
-o jsonpath='{range .items[*]}{"\n"}
{.metadata.name}{"\n"}
{range .spec.containers[*]}{"  - "}{.image}{"\n"}{end}{end}'
```

### Check the AID

```
kubectl exec deployment/falcon-kac -n falcon-kac -c falcon-ac -- falconctl -g --aid
```

Details about these commands (and other troubleshooting steps) can be found here:
[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac)

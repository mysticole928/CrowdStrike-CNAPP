# CrowdStrike Falcon
## Kubernetes Admission Controller Helm Chart
## Falcon KAC

The official repo for the CrowdStrike helm charts is on github.

Here is the URL:

[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac)

## API Keys

An API key from Falcon is needed in order to download the sensor.

Falcon Kubernetes Admission Controller (KAC) API Scopes

- `Falcon Images Download`: Read
- `Sensor Download`: Read

## Helm requirements

- Helm 3.x is installed and available in PATH
- Helm 3.x is supported by the Kubernetes distribution
- The cluster is running a supported x86_64 Kubernetes environment

# Verify the Falcon KAC is Running

_These steps are optional._

To verify that the Falcon KAC is running use this command:

```bash
kubectl get deployments, pods -n falcon-kac
```

This will display the deployment: `falcon-kac`.
It will also show a pod name that starts with `falcon-kac`.  

An agent ID (AID) is assigned to the Falcon KaC when it communicates with the Falcon cloud.

If the Falcon KAC has a valid AID, this means it has been installed and is running properly.

To view the AID use this command:

```bash
kubectl exec deployment/falcon-kac -n falcon-kac -c falon-ac -- falconctl -g --aid
```

`kubectl` options:

- `exec (POD | TYPE/CONTAINER)` - Execute a command inside a running container
- `-n`: Specify a namespace
- `-c`: Specify a container
- `--`: End of `kubectl` options
- `falconctl -g --aid`: The command passed to the container

The `falcontl` option `-g` will GET information from the sensor.

- `--aid`: The Agent ID (AID)
- `--cid`: The Cusomter ID (CID) without the checksum

# Troubleshooting

- Verify the image name and image tag are set correctly
- Be sure the image is available in either the local/remote registry
- Verify the `ImagePullPolicy` is set correctly on the cluster

## View the logs from a Kubenetes POD

To view the rolling logs from a Kubernetes pod use the `logs` command
with `kubectl`.

```bash
kubectl logs -f [POD-NAME] -n NAMESPACE
```


# CrowdStrike Falcon
## Kubernetes Admission Controller Helm Chart
## Falcon KAC

Updated: 2024-07-24
Moved to new folder for navigation/readability.  Eventually, the Helm information will be split from this file and moved into its own folder.

Updated: 2024-04-26
Minor edits to fix typos, added additional information for troubleshooting, and included an example of helm install with `falcon.tags`. 

The official repo for the CrowdStrike Kubernetes Admission Controller helm charts is on github.  

Here is the URL:

[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac)

The notes on this page are based _entirely_ on those public-facing resources.

## API Keys

An API key from Falcon is needed in order to download the sensor.

Falcon Kubernetes Admission Controller (KAC) API Scopes

- `Falcon Images Download`: Read
- `Sensor Download`: Read

## Helm requirements

- Helm 3.x is installed and available in PATH
- Helm 3.x is supported by the Kubernetes distribution
- The cluster is running a supported x86_64 Kubernetes environment

# Install the Falcon KAC

## Add the CrowdStrike Falcon Helm Repository

```bash
helm repo add crowdstrike https://crowdstrike.github.io/falcon-helm
```

## Update the Falcon Helm Repository Cache

```bash
helm repo update
```

## Set Environmental Variables for the Falcon KAC image repository, image tag, and Falcon CID

```bash
export KAC_IMAGE_REPO=<registry_name>/falcon-kac
export KAC_IMAGE_TAG=<KAC_version>.container.x86_64.Release.<cloud_region>
export FALCON_CID=<your_CID_with_checksum>
```

# Install the Falcon KAC Helm Chart

The `--set flag` passes parameter values to helm.

This example uses the linux environmental variables set in the previous section.  

The `-n` option specifies a Kubernetes namespace.  `--create-namespace` will create it if needed.

```bash
 helm install falcon-kac crowdstrike/falcon-kac \
  -n falcon-kac --create-namespace \
  --set falcon.cid=$FALCON_CID \
  --set image.repository=$KAC_IMAGE_REPO \
  --set image.tag=$KAC_IMAGE_TAG
```

## Verify the Falcon KAC Install

```bash
kubectl get deployments,pods -n falcon-kac
```

**Note:** There are **NO** spaces between `deployments` and `pods`. 

## Verify the Falcon KAC AID

```bash
 kubectl exec deployment/falcon-kac -n falcon-kac -c falcon-ac -- falconctl -g --aid
```

# Update the Falcon KAC

When a new container image is available, update the Falcon KAC by passing the new container image to the Helm chart and running a helm upgrade command. 

Updates to the Falcon KAC must be done manually.  This can be done directly on a Kubernetes cluster or update through a CI/CD pipeline.

```bash
helm upgrade --install falcon-helm crowdstrike/falcon-kac \
     -n falcon-kac \
     --set falcon.cid=<FALCON_CID> \
     --set image.repository=<KAC_REPO> \
     --set image.tag=<KAC_TAG>
```

## If the Falcon KAC Update Fails

If the KAC update process has an error, the easist fix is to remove it and then reinstall.

```bash
helm uninstall falcon-kac -n falcon-kac
```

# Troubleshooting

- Verify the image name and image tag are set correctly
- Be sure the image is available in either the local/remote registry
- Verify the `ImagePullPolicy` is set correctly on the cluster

## Verify the Falcon KAC is Running

_These steps are optional._

To verify that the Falcon KAC is running use this command:

```bash
kubectl get deployments,pods -n falcon-kac
```

This will display the deployment: `falcon-kac`.
It will also show a pod name that starts with `falcon-kac`.  

An agent ID (AID) is assigned to the Falcon KAC when it communicates with the Falcon cloud.

If the Falcon KAC has a valid AID, this means it has been installed and is running properly.

To view the AID use this command:

```bash
kubectl exec deployment/falcon-kac -n falcon-kac -c falcon-ac -- falconctl -g --aid
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

## View the logs

To view the rolling logs from a Kubernetes pod use the `logs` command
with `kubectl`.

This is the format of the `kubectl logs` command

```bash
kubectl logs -f [POD-NAME] -n NAMESPACE
```

To get the most recent Falcon KAC logs:

```bash
kubectl logs -l app=falcon-kac -n falcon-kac --all-containers --tail=-1
```

Get the most recent Falcon KAC log entries and save them to a file name `falcon-kac.log`:

```bash
kubectl logs -l app=falcon-kac -n falcon-kac --all-containers --tail=-1 > falcon-kac.log
```

## Gather information about all falcon-kac resources

```bash
kubectl get all -n falcon-kac
```

## Get the Kubernetes cluster ID

The `ClusterId` can be used instead of `ClusterName` to search both the Host Management UI and the Kubernetes IOM UI.

```bash
kubectl get ns kube-system --output=jsonpath={.metadata.uid}
```

## Use Falcon Tags to create dynamic Host Groups for Falcon Admissions Control Policies

Instead of depending on the Kubernetes hostname to create a dynamic Host Group, it's possible to add a Falcon Tag to the Falcon KAC.

When using a Helm chart, tags are added with the `--set` option and `falcon.tags`.

Multiple tags can be added in a single statement.  They are separated with commas (`,`) that must be escaped with a backslash (`\`) character.

For example: `--set falcon.tags="tag-1\,tag-2\,tag-3"

Here's the `helm` command with tags added.

```bash
helm upgrade --install falcon-kac crowdstrike/falcon-kac \
     -n falcon-kac --create-namespace \
     --set falcon.cid=$FALCON_CID \
     --set image.repository=$FALCON_REPO \
     --set image.tag=$FALCON_IMAGE_TAG \
     --set falcon.tags="eks-cluster"
```



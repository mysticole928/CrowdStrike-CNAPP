# Falcon Image Analyzer

Created: 2024-02-12
Updated: 2024-04-02 Fixed some typos and changed filename.

This feature is offically called the **Image Assessment at Runtime** or **IAR**.

## Official CrowdStrike Falcon Image Analyzer Github Repo

The official GitHub repo for the Falcon Image Analyzer is here:

[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-image-analyzer](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-image-analyzer)

The notes on this page are informational.  When in doubt, consult the official documentation.

## Falcon API Scopes

The Falcon Image Analyzer reqiores a CrowdStrike API client key with these scopes:

- Falcon Container CLI (Write)
- Falcon Container Image (Read/Write)
- Falcon Images Download (Read)

## List the Falcon Image Analyzer Versions

The `falcon-container-sensor-pull.sh` script is used to download the image analyzer container.

[The Falcon Container Sensor Pull Script GitHub Repo](https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull)

### Environmental Variables

These examples use unvironmental variables to specify the the Falcon Client ID, 
the Falcon Client Secret, the Falcon CID, the cloud region, and the Falcon cloud 
api endpoint.

Change these values to the appropriate ones.

```bash
export FALCON_CID=1234567890-12
export FALCON_CLIENT_ID=abcdef0123456789
export FALCON_CLIENT_SECRE=Tabcdef0123456789
export FALCON_CLOUD_REGION=us-1
export FALCON_CLOUD_API=api.crowdstrike.com
```

### List Available Versions

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-imageanalyzer \
--list-tags
```

Note: For this to work, _omit_ the option `--platform`.  This option is used for the Falcon Sensor.

Possible output:

```bash
{
  "name": "falcon-imageanalyzer",
  "repository": "registry.crowdstrike.com/falcon-imageanalyzer/us-1/release/falcon-imageanalyzer",
  "tags": [
     "0.42.0",
     "1.0.0",
     "1.0.1",
     "1.0.2",
     "1.0.3" 
  ]
}
```

### Download the Latest Falcon Image Analyzer

To download the most recent image analyzer:

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-imageanalyzer
```

If using `docker`, it must be running first.

### Download a Specific Image Analyzer Version

To download a specific version, specify the appropriate tag with the `--version` argument.

For example, to download the version tagged `1.0.2`:

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-imageanalyzer \
--version "1.0.2"
```

### Copy the Image Analzyer Directly to a Registry

To copy the image analyzer to a specific container registry, use the `--copy` argument.

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-imageanalyzer \
--copy registry.uri.without.repository.name
```

## Install the Falcon Image Analyzer using Helm

Ensure that the `helm` repo is installed and up to date.

```bash
helm repo add crowdstrike https://crowdstrike.github.io/falcon-helm
helm repo update
```

### Watcher Mode

Watcher Mode is the recommended mode to run the Falcon Image Analyzer and is designed to run as a 
Kubernetes Deployment with a replica of 1. 

When deployed to a Kubernetes cluster, it runs on a single node in the cluster. 

The Image Assessment and Runtime (IAR) agent connects to the Kubernetes API using an assigned RBAC 
permission to retrieve pod info. 

When an image is started on a node, the IAR agent pulls the image to a separate container to 
read the image and do its analysis. 

### Socket Mode

This deployment mode is for when Watcher Mode is not suitable for an environment.

Socket Mode connects to the container runtime socket.  This could be Docker, Podman, containerd, or CRI-O. 

When Image Assessment and Runtime (IAR) is deployed to a Kubernetes cluster in Socket Mode, it’s deployed 
as a Kubernetes DaemonSet resource and lets the IAR agent connect to the runtime on each node in the 
cluster. 

When IAR is deployed to a standalone Linux host, the IAR agent runs as a container on the host and connects to the container runtime socket.

Consult the documentation for details.

### Install the Image Analyzer from a Specific Registry: Node-Based Sensors

Watcher mode is enabled using `--set deployment.enabled=true`.

```bash
helm upgrade --install falcon-image-analyzer crowdstrike/falcon-image-analyzer \
  -n falcon-image-analyzer --create-namespace \
  --set crowdstrikeConfig.cid=$FALCON_CID \
  --set crowdstrikeConfig.clientID=$FALCON_CLIENT_ID \
  --set crowdstrikeConfig.clientSecret=$FALCON_CLIENT_SECRET \
  --set image.repository="image.respository.uri/falcon-imageanalyzer" \
  --set image.tag="1.0.3" \
  --set deployment.enabled=true \
  --set crowdstrikeConfig.clusterName="cluster/kubernetes-cluster-name"
```

### Install the Image Analyzer from a Specific Registry: Container-Based (Sidecar) Sensors

When using the Container-based (Sidecar) sensor, disable the Falcon Container Sensor in the
image analyzer namespace to prevent it from being injected.

`--set podAnnotations."sensor\.falcon-system\.crowdstrike\.com/injection"=disabled`

**Important**: Be sure to escape the period (`.`) character with a backslash (`\`) inside the argument.

```bash
helm upgrade --install falcon-image-analyzer crowdstrike/falcon-image-analyzer \
  -n falcon-image-analyzer --create-namespace \
  --set crowdstrikeConfig.cid=$FALCON_CID \
  --set crowdstrikeConfig.clientID=$FALCON_CLIENT_ID \
  --set crowdstrikeConfig.clientSecret=$FALCON_CLIENT_SECRET \
  --set image.repository="image.repository.uri/falcon-imageanalyzer" \
  --set image.tag="1.0.3" \
  --set deployment.enabled=true \
  --set podAnnotations."sensor\.falcon-system\.crowdstrike\.com/injection"=disabled \
  --set crowdstrikeConfig.clusterName="cluster/kubernetes-cluster-name
```

## Pod Security Standards

Starting with Kubernetes 1.25, Pod Security Standards are enforced. 

To set the appropriate Pod Security Standards policy, add a label to the namespace.

```bash
kubectl label --overwrite ns falcon-imageanalyzer \
  pod-security.kubernetes.io/enforce=privileged
```

_Optional_: To silence the warning and change the auditing level for the Pod Security Standard, add the following labels:

```bash
kubectl label ns --overwrite falcon-imageanalyzer pod-security.kubernetes.io/audit=privileged
kubectl label ns --overwrite falcon-imageanalyzer pod-security.kubernetes.io/warn=privileged
```

## View IAR Resource Consumption

```bash
kubectl top pod -n falcon-image-analyzer
```

## Delete the Image Analyzer 

To delete the image analyzer:

```bash
helm uninstall falcon-image-analyzer -n falcon-image-analyzer && kubectl delete namespace falcon-image-analyzer
```








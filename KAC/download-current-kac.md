# Installing the CrowdStrike Falcon KAC

Updated: 2024-10-22

Disclaimer: These are my notes based on work that I've done building a training environment.  They are to be used as a reference and are *_not_* the official source of truth.

Here is the link to the official Falcon Container Sensor Pull Script:

[https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull](https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull)

## Shell Variables

The command examples have be parameterized.  Here are the environmental variables that were set in advance.

```
export FALCON_CLIENT_ID=<falcon-client-id>
export FALCON_CLIENT_SECRET=<falcon-client-secret>
export FALCON_CID=<falcon-cid-with-checksum>
export FALCON_CLOUD_REGION=<falcon-cloud-region>
export FALCON_CLOUD_API=<falcon-cloud-api-endpoint>
export PRIVATE_REGISTRY=<url-for-container-registry>
```

## List the available versions of the Falcon KAC

```shell
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-kac \
--list-tags
```

Note: `--client-id` and `--client-secret` are required.

## Download Current Falcon KAC

```shell
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-kac
```

Docker (or similar software) must be running.

## Copy the Falcon KAC to a Private Registry

```shell
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-kac \
--copy $PRIVATE_REGISTRY
```

The `--copy` argument only needs the regustry URL.  The repository name is set by the `--type` argument.

## Install the Falcon KAC from a Private Registry

### First, assign the tag to a shell variable.

This command returns the registry, repository, and tag:

```./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --region $FALCON_CLOUD_REGION \
  --type falcon-kac \
  --get-image-path
```

Parse it with the linux `cut` command:

```
export KAC_TAG=$(./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --region $FALCON_CLOUD_REGION \
  --type falcon-kac \
  --get-image-path | cut -d ':' -f 2)
```

Verify the output:

`echo $KAC_TAG`

### Install the Helm Chart

Currently, these are the requirements to install and deploy the Falcon KAC using Helm:

- Helm 3.x must be installed and in the PATH
- Helm 3.x must be supported by the Kubernetes distribution
- The Kubernetes cluster must using an x86_64 environment

Add the CrowdStrike Helm repository:

```
helm repo add crowdstrike https://crowdstrike.github.io/falcon-helm && helm repo update
```

**Important:** Before updating the Falcon KAC, sensor, or IAR, **always** run `helm repo update` first.

### Install the Falcon KAC

The Falcon KAC might not be able to read the metadata with the cluster name.

To ensure it gets assigned the correct Falcon Host Group for the Kubernetes Admission Controller policy, use sensor grouping tag.

Use `--set falcon.tags` to assign tag values.  Separate multiple tag values with a comma.  The backslash before the comma prevents it from being seen as part of the shell command.

```shell
helm upgrade --install falcon-kac crowdstrike/falcon-kac \
     -n falcon-kac --create-namespace \
     --set falcon.cid=$FALCON_CID \
     --set image.repository=$PRIVATE_REGISTRY/falcon-kac \
     --set image.tag=$KAC_TAG \
     --set falcon.tags="tag-1\,tag-2\,tag-3\,tag-4"
```

A message like this one will appear:

```
Release "falcon-kac" does not exist. Installing it now.
NAME: falcon-kac
LAST DEPLOYED: Tue Oct 22 14:33:31 2024
NAMESPACE: falcon-kac
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
Thank you for installing the CrowdStrike Falcon Kubernetes Admission Controller!

Note that in order for the Falcon Kubernetes Admissions Controller to run, the
falcon-kac image must be present in a container registry accessible to the
kubernetes deployment.

When utilizing your own registry, a common error on installation is forgetting
to add your containerized sensor to your local image registry prior to
executing `helm install`. Please read the Helm Chart's readme for more
deployment considerations.

To check the status of Falcon Kubernetes Admissions Controller pods, run the
following command:

  kubectl -n falcon-kac get pods

```

Verify the installation:

`kubectl -n falcon-kac get pods`

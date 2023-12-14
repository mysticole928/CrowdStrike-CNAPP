# Falcon Container Downloads

2023-11-15

It's possible to download the latest **Falcon Container Sensor**, the **Falcon Node Sensor**, the **Falcon Kubernetes Admission Controller**, and the **Falcon Kubernetes Protection Agent** from the **CrowdStrike** container registry.

## Prerequisites

## Software Install

- `curl`
- `docker`, `podman`, or `skopeo`

To download container images locally, Docker (or something like it) needs to be running before using the **Falcon Container Sensor Pull Script**.  

## Falcon API Client

To download the Falcon Sensor (node), the Falcon Container Sensor (container), or the Kubernetes Admission Controller an `API Client` inside Falcon needs to be created withe these scopes:

- Falcon Images Download (Read)
- Sensor Download (Read)

To download the Falcon Kubernetes Protection Agent this scope is also needed:

- Kubernetes Protection (Read)

## Download the Falcon Containder Pull Script

The script to pull the container images is here:

[The Falcon Container Sensor Pull Repo](https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull)

## Usage

After downloading the pull script and making it executable, view the possible options by using the `--help` option.

`./falcon-container-sensor-pull.sh`

```
usage: falcon-container-sensor-pull.sh

Required Flags:
    -u, --client-id <FALCON_CLIENT_ID>             Falcon API OAUTH Client ID
    -s, --client-secret <FALCON_CLIENT_SECRET>     Falcon API OAUTH Client Secret

Optional Flags:
    -f, --cid <FALCON_CID>            Falcon Customer ID
    -r, --region <FALCON_REGION>      Falcon Cloud
    -c, --copy <REGISTRY/NAMESPACE>   registry to copy image e.g. myregistry.com/mynamespace
    -v, --version <SENSOR_VERSION>    specify sensor version to retrieve from the registry
    -p, --platform <SENSOR_PLATFORM>  specify sensor platform to retrieve e.g x86_64, aarch64
    -t, --type <SENSOR_TYPE>          specify which sensor to download [falcon-container|falcon-sensor|falcon-kac|kpagent]
                                      Default is falcon-container.

    --runtime                         use a different container runtime [docker, podman, skopeo]. Default is docker.
    --dump-credentials                print registry credentials to stdout to copy/paste into container tools.
    --list-tags                       list all tags available for the selected sensor
    --allow-legacy-curl               allow the script to run with an older version of curl

Help Options:
    -h, --help display this help message
```

If you omit the `--type` option, the default is `falcon-container`.

**To avoid confusion, always specify the sensor type to download.**

## Environmental Variables

To make the script easier to read/manage, save the Falcon Client ID, Client Secret, Falcon CID, the Falcon Cloud Region, and Falcon API url as environmental variables.

The cloud region and api url depend on where has been provisioned.  When the Falcon API Client is provisioned, this information will be provided.

```
export FALCON_CLIENT_ID=1234567890abcdef
export FALCON_CLIENT_SECRET=fedcba0987654321
export FALCON_CID=a1b2c3d4e5f6-68
export FALCON_CLOUD_REGION=us-1
export FALCON_CLOUD_API=api.crowdstrike.com
```

If you're new to shell scripting, the `export` command ensures environmental variables are passed to any shells that are spawned/created.  It's optional but can save some frustration in some cases.

Also, the backslash `\` is a line-continuation character in linux/unix. It's used in these example to make them readable.

## Falcon Kubernetes Protection Agent

The Falcon Kubernetes Protection agent is automatically installed as part of registration process.  However, it's possible to download the image and save it locally or in a private repository.

```
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION
--type kpagent
```

Unlike other container image downloads, only the latest version is available.  _(As of this writing.)_  If you try to list the tags (the versions), it will return an error.

### List the Available KAC container versions

The following script will use the environmental variables created above and choose the `x86-64` cpu architecture to list all of the available versions.

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-kac \
--platform x86_64 \
--list-tags
```

### Download the current KAC version and copy it directly to a specific registry

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-kac \
--platform x86_64 \
--copy my.registry.url
```

**Note: The container registry URL is only the base URL.  The image _name_ and _tag_ (the version) are copied from the CrowdStrike registry automatically.**

## The Falcon Node Sensor

Notice that the `--type` is `falcon-sensor` for both the node-based sensor and the container-based (sidecar) sensor.

When **node** and **container** images are pulled from the CrowdStrike registry, they both have the name `falcon-sensor`. 
The **tag** for the `falcon-container` image includes the word _container_.

### List Available Versions

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-sensor \
--platform x86_64 \
--list-tags
```

### Download the current node sensor and save it to the local container registry

In these examples, the `--type` is `falcon-sensor`.

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-sensor \
--platform x86_64
```

### Pull current node sensor and copy it to a specific registry

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-sensor \
--platform x86_64 \
--copy myregistry.url.com # <-- No repository or tag
```

## The Container Sensor

In these examples, the `--type` is `falcon-container`.

### Pull the current container sensor and save it to the local container registry

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-container \
--platform x86_64
```

### Pull the most current container sensor to a specific registry

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-container \
--platform x86_64 \
--copy myregistry.url.com # <-- No repository or tag name
```




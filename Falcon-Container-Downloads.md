# Falcon Container Downloads

Created: 2023-11-15

Updated: 

2024-02-02 - Added information about the falcon-imageanayzer
2024-02-08 - Fixed an instruction about excluding the `--platform' argument when download the Image Analyzer


It's possible to download the latest **Falcon Container Sensor**, the **Falcon Node Sensor**, the **Falcon Kubernetes Admission Controller**, the **Falcon Kubernetes Protection Agent**, and the **Falcon Image Analyzer** from the **CrowdStrike** container registry.

## Prerequisites

## Software Install

- `curl`
- `docker`, `podman`, or `skopeo`

When using Docker, it must be running locally.

## Falcon API Client

To download the Falcon Sensor (node), the Falcon Container Sensor (container), or the Kubernetes Admission Controller an `API Client` inside Falcon needs to be created withe these scopes:

- Falcon Images Download (Read)
- Sensor Download (Read)

To download the Falcon Kubernetes Protection Agent this scope is also needed:

- Kubernetes Protection (Read)

This scope is required for the Kubernetes Protection Agent and the Kubernetes Admission Controller.

To use the Falcon Image Analyzer these scopes are required:

- Falcon Container CLI (Write)
- Falcon Container Image (Read/Write)
- Falcon Images Download (Read)

## Download the Falcon Containder Pull Script

The official GitHub repo for the script that pulls the container images is here:

[The Falcon Container Sensor Pull Repo](https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull)

To download the script using `curl`:

```bash
curl -O https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh
```

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
    -t, --type <SENSOR_TYPE>          specify which sensor to download [falcon-container|falcon-sensor|falcon-kac|falcon-snapshot|falcon-imageanalyzer|kpagent]
                                      Default is falcon-container.

    --runtime                         use a different container runtime [docker, podman, skopeo]. Default is docker.
    --dump-credentials                print registry credentials to stdout to copy/paste into container tools.
    --get-image-path                  get the full image path including the registry, repository, and latest tag for the specified SENSOR_TYPE.
    --get-pull-token                  get the pull token of the selected SENSOR_TYPE for Kubernetes.
    --get-cid                         get the CID assigned to the API Credentials.
    --list-tags                       list all tags available for the selected sensor type and platform(optional)
    --allow-legacy-curl               allow the script to run with an older version of curl
```

If the `--type` option is omitted it will default to `falcon-container`.

The `--runtime` option defaults to `docker`

When downloading the `falcon-imageanalyzer` omit the `--platform` option.

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

## The Container Sensor (Sidecar)

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

## Falcon Image Analyzer

### Get version information

To see the verison information, use the `--list-tags` option.

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-imageanalyzer \
--list-tags
```

### Pull the image

```bash
./falcon-container-sensor-pull.sh \
--client-id $FALCON_CLIENT_ID \
--client-secret $FALCON_CLIENT_SECRET \
--region $FALCON_CLOUD_REGION \
--type falcon-imageanalyzer
```

Note: Omit the `--platform` option.


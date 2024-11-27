# Download and Install the Falcon Node-Sensor

## Install and Update Helm

```shell
helm repo add crowdstrike https://crowdstrike.github.io/falcon-helm && helm repo update
```

Before upgrading any Falcon container, **always** run `helm repo update` **FIRST**.

## List the Sensor Version

```shell
./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --type falcon-sensor \
  --list-tags
```

The `--type falcon-sensor` is for node-based deployments.  For the sidecar/injected install, the type is `falcon-container`.

### Copy the Multi-Architecture Falcon Sensor Container to a Private Registry

```
./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --type falcon-sensor \
  --copy $PRIVATE_REGISTRY
```

It is possible to install the sensor from the CrowdStrike registry.  However, the best practice is to pull the image locally first.  

The current node-based sensor images have both Intel and ARM architectures in them.  Docker does **NOT** support multi-architecture images.  

To specify an architecture with the `falcon-container-sensor-pull.sh` script, use the argument: `--platform` 

### Get the Latest Sensor Version and Tag

```shell
./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --type falcon-sensor \
  --get-image-path
```

#### Get Tag/Version

This uses the linux `cut` command to get all the data after the colon (`:`) in the image path.

```shell
./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --region $FALCON_CLOUD_REGION \
  --type falcon-sensor \
  --get-image-path | cut -d ':' -f 2
```

#### Save the Tag/Version in a Shell Variable

```
export SENSOR_TAG=$(./falcon-container-sensor-pull.sh \
  --client-id $FALCON_CLIENT_ID \
  --client-secret $FALCON_CLIENT_SECRET \
  --region $FALCON_CLOUD_REGION \
  --type falcon-sensor \
  --get-image-path | cut -d ':' -f 2)
```

Test the output:

```shell
echo $SENSOR_TAG
```

## Install the Falcon Node Sensor Using Helm

```shell
helm upgrade --install falcon-helm crowdstrike/falcon-sensor \
 -n falcon-system --create-namespace\
 --set node.enabled=true \
 --set container.enabled=false \
 --set falcon.cid=$FALCON_CID \
 --set node.image.repository=$PRIVATE_REGISTRY/falcon-sensor \
 --set node.image.tag=$SENSOR_TAG \
 --set falcon.tags="Tag1\,Tag2\,Tag3"
```

## Sensor Grouping Tags

When using sensor grouping tags to assign Falcon Host Groups, they can be assigned using Helm.  

Use `--set falcon.tags` to assign sensor grouping tags.  Be sure to enclose the tags with quotation (`" "`) marks.  Multiple tags must be separated with a comma (`,`) and the commas must be "escaped" with a backslash (`\`) otherwise the shell will parse the command incorrectly.



# General Setup Considerations

## Official CrowdStrike GitHub Repository

Get the newest version of the container pull script from the CrowdStrike GitHub repository.  

When in doubt, check this page for updates and/instructions.

[https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull](https://github.com/CrowdStrike/falcon-scripts/tree/main/bash/containers/falcon-container-sensor-pull)

To download the current pull script:

```shell
curl --silent --show-error --location "https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh"
```

In the `scripts` folder is a shell script that will download the most recent pull script from the CrowdStrike GitHub repository.

If the pull script exists locally, it will check the version information.  When there is a new version, it will replace the existing script and archive the old one.

## Helm 

Helm is a package manager for Kubernetes. 

When using Helm, remember to include `helm repo update` before updating the Falcon Cloud Security containers.

It's in the instructions but it can be easy to overlook.

### Command to add the CrowdStrike Helm Repository

```shell
helm repo add crowdstrike https://crowdstrike.github.io/falcon-helm && helm repo update
```

### Update the Helm Repository before updating the FCS containers

Worth repeating.

```shell
helm repo update
```

## The KAC and IAR use different parameter names for the same options

For example, IAR uses `crowdstrikeConfig.cid` to set the CID information.

The KAC and Falcon Sensor (Container and Node) use `falcon.cid`.

### Falcon Sensor Helm Chart GitHub Page

[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-sensor](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-sensor)

### Falcon IAR Helm Chart GitHub Page

[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-image-analyzer](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-image-analyzer)

### Falcon KAC Helm Chart GitHub Page

[https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac](https://github.com/CrowdStrike/falcon-helm/tree/main/helm-charts/falcon-kac)

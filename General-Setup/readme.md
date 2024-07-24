# General Setup Considerations

## Shell Variables

When working with Kubernetes and the command line, shell variables
minimize human error and help with automation.

Some to consider creating:

```bash
export FALCON_CLIENT_ID=
export FALCON_CLIENT_SECRET=
export FALCON_CID=
export FALCON_CLOUD_REGION=
export FALCON_CLOUD_API=
export PRIVATE_REGISTRY=
```

If a process/command creates a new shell, the `export` command ensures
they variable is available in that shell.

## Helm 

Helm is a package manager for Kubernetes.  There are other package managers.

When using Helm, remember to include `helm repo update` before updating the 
Falcon Cloud Security containers.

It's in the instructions for registering Kubernetes clusters but it can be
easy to omit.

### Command to add the CrowdStrike Helm Repository
```shell
helm repo add crowdstrike https://crowdstrike.github.io/falcon-helm && helm repo update
```

### Update the Helm Repository before updating the FCS containers
```shell
helm repo update
```

# Shell Variables

When working with the Falcon sensor download, use environmental variables
to minimize errors.

The command examples in this repo use one or more of the following:

```shell
export FALCON_CLIENT_ID=<falcon-api-client-id>
export FALCON_CLIENT_SECRET=<falcon-api-client-id-secret>
export FALCON_CID=<falcon-cid-with-check-sum>
export FALCON_CLOUD_REGION=<falcon-cloud-region>
export FALCON_CLOUD_API=<falcon-cloud-api-url>
export PRIVATE_REGISTRY=<private-registry-url>
```

For anyone new to shell variables, the `export` option ensures variables created
are part of any new shell spawned by a command.

For the Falcon scripts, this shouldn't happen. 

# Python Scripts for Managing Kubernetes and Containers

## `deploy.py`

The script `deploy.py` runs  Kubernetes deployment files defined by `DEFAULT_FILE_PATTERN`
The default pattern is `*.yaml`.

To start the deployments: `./deploy.py create`
To delete/stop the deployments: `./deploy.py delete`

The `create` option is the equivalent of: `kubectl apply -f *.yaml`
The `delete` option is the equivalent of: `kubectl delete -f *.yaml`
Without any arguments, it displays output equivalent to `kubectl get deployments --all-namespaces`

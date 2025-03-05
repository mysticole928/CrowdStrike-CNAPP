# Python Scripts for Managing Kubernetes and Containers

## `deploy.py`

The script `deploy.py` runs all the Kubernetes deployment files ending in `.yaml` in a directory.

To start the deployments: `./deploy.py start`
To delete/stop the deployments: `./deploy.py stop`

The `start` option is the equivalent of: `kubectl apply -f *.yaml`
The `stop` option is the equivalent of: `kubectl delete -f *.yaml`

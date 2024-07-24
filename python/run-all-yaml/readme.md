# Run All YAML

The python scripts in this folder will run or all the kubernetes `yaml` files in a given directory.

They are used to build or tear down my lab evironment and are rudimentary.  There is no error checking or advanced processing.

They get a listing of the `.yaml` files in the current directory and send them to `kubectl`.

`k8s-add-pods.py` - Runs `kubectl apply -f <filename>.yaml`
`k8s-delete-pods.py` - Runs `kubectl delete -f <filename>.yaml`

## To Do

Add:
- Error checking
- Logic from the KAC IOM shell script `falcon-kac-output.sh`

# Falcon KAC Output Script

The default output of the KAC's IOM messages is difficult to read.

<img width="1000" alt="Falcon-KAC-Default-Output" src="https://github.com/user-attachments/assets/494a32f7-c054-436e-ae42-da59c71969e0">

The `falcon-kac-output.sh` makes it easier to read and saves the contents to a local logfile.

## The Warnings

<img width="1000" alt="Falcon-KAC-Warnings" src="https://github.com/user-attachments/assets/019af04b-b755-4981-9e95-afe5f320a3f2">


## The Preventions

<img width="1000" alt="Falcon-KAC-Preventions" src="https://github.com/user-attachments/assets/21eb50b9-d995-4661-94a8-562ba6c15a10">


## Running the Script

The script is designed to take the output of either `kubectl create` or `kubectl apply` and reformat it.

To run it:

```shell
kubectl apply -f deployment_file_name.yaml 2>&1 | ./falcon-kac-output.sh
```

The `2>&1` is easy to overlook.

## Create an Alias

To make the script easy to run and avoid modifying the `path variable, create a scripts directory and put it there.

Then, create an alias:

```shell
alias kapply="function _kapply(){ kubectl apply -f \$1 2>&1 | ~/scripts/falcon-kac-output.sh; }; _kapply"
```

In this example, the script is in the `~/scripts` directory.

The alias contains a shell function that reads a filename as its argument and passes it to `kubectl`.

Usage:

```shell
kappy deployment_file_name.yaml
```

Boom!

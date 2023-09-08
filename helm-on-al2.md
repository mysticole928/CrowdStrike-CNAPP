# Install Helm

This explains how to install Helm on Amazon Linux 2.  It's designed to help people
that are unfamiliar with the linux command line.

## Official Docs

The Helm install information from AWS is here:

[https://docs.aws.amazon.com/eks/latest/userguide/helm.html](https://docs.aws.amazon.com/eks/latest/userguide/helm.html)

## Download Install Script

To install Helm on AL2, download the install script:

```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 > get_helm.sh
```

Instead of the `-o` flag with `curl`, this example redirects the output with the `>` symbol.

## Make the script executable

Make `get_helm.sh` executable using the `chmod` command:

```bash
chmod 700 get_helm.sh
```

## Run the Installer

Run `get_helm.sh` to install it:

```bash
./get_helm.sh
```

**Alternatively**, `helm` can be installed in one step:

```bash
curl -sSL https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

## Test the Install

To test the install:

```bash
helm version --short
```

A less verbose way of getting the `helm` version:

```bash
helm version --short | cut -d + -f 1
```

If `helm` doesn't work, log out and log back in again to update the `PATH`
variable.

## Configure Bash completion for `helm` (Optional)

```bash
helm completion bash >> ~/.bash_completion
. /etc/profile.d/bash_completion.sh
. ~/.bash_completion
source <(helm completion bash)
```

The first three lines adds `helm` autocomplete to the `bash` shell. It will be
available in future logins.

The last line--the one that starts with `source`--loads completions in the
current shell.

For more information about `helm` completion:

[https://helm.sh/docs/helm/helm_completion_bash/](https://helm.sh/docs/helm/helm_completion_bash/)

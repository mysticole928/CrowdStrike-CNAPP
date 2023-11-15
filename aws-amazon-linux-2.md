# AWS Amazon Linux 2

Amazon Linux 2 comes with version 1 of the `awscli` installed.

When using an EC2 instance running Amazon Linux 2 to create/register
kubernetes clusters, update the CLI first!

## Update Amazon Linux 2

Update AL2 first.

```bash
sudo yum update -y && sudo yum upgrade -y
```

If you're new to linux, this is what that command does:

- `yum update -y` updates all the currently installed packages.
- `yum upgrade -y` upgrades the packages with updates and removes obsolete ones.

The `-y` automatically responds to the yes/no prompt built into `yum`.

The `&&` syntax is specific to `bash` and runs the second command only if the
first one is successful.

The official AWS documentation to update the AWS CLI is here:

[https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

## Remove the existing AWS CLI

There are some `awscli` sym-links that should be removed before updating.

```bash
sudo yum remove awscli
```

## Download the Latest Version

Here's the command to download the most recent version of the AWS CLI:

### x86_64

[curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"](curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip")

### ARM

[curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"](curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip")

The curl option `-o` specifies the output filename.

## Unzip the Archive

```bash
unzip awscliv2.zip
```

If there's an existing archive, it's possible to overwrite it with the updated files.
Use the `-u` option.

```bash
 unzip -u awscliv2.zip
```

## Run the Installer

```bash
sudo ./aws/install
```

## Verify the Install

```bash
aws --version
```

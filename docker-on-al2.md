# Install Docker on Amazon Linux 2

## Use `yum` to Install Docker

To install `docker` on Amazon Linux 2, run this command:

```bash
sudo yum install docker -y
```

## Update the ec2-user linux group information

Add group membership for the `ec2-user` to run `docker` commands without
needing `sudo`.

```bash
sudo usermod -a -G docker ec2-user
```

Reload the `ec2-user` linux group assignments to `docker` without logging
out and back in again.

```bash
id ec2-user
newgrp docker
```

The `newgrp` command changes a user's real group identification.

The command opens a new shell changes the name of `real` group to the one
specified.

## Enable the docker service at boot

```bash
sudo systemctl enable docker.service
```

## Start the docker service

```bash
sudo systemctl start docker.service
```

## Verify the docker service is running

```bash
sudo systemctl status docker.service
```

## systemctl commands for docker

```bash
sudo systemctl start docker.service #<-- Start the service
sudo systemctl stop docker.service #<-- Stop the service
sudo systemctl restart docker.service #<-- Restart the service
sudo systemctl status docker.service #<-- Get the service status
```

## Start the docker service

```bash
sudo systemctl start docker.service
```

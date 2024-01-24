# Trigger an IOA from the CLI

2024-01-24

## Introduction

This document describes how to trigger an Indicator of Attack (IOA) inside Falcon Cloud Security (FCS) CSPM.  

It uses the AWS Command Line tools and the program `jq`.

`jq` is a lightweight and flexible command-line JSON processor.

- AWS CLI: [https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- `jq`: [https://jqlang.github.io/jq/](https://jqlang.github.io/jq/)

To trigger the IOA, have at least one EC2 instance running and permission to change its security group.

## Think Like a Bad Actor

The way this works is to behave like a bad actor.  A bad actor is--very likely--going to probe an environment to see what's inside.  

Someone that created an environment will know its contents and how to connect to them.

## Find Running EC2 Instances

Start by probing a region for running EC2 instances.

```bash
aws --profile <profile-name> ec2 describe-instances \
--region <aws-region> \
--filters "Name=instance-state-name, Values=running" \
--output yaml
```

If the AWS CLI has multiple profiles, use `--profile` to choose the correct one.  _This is optional_.  

The `--filters` argument t does server-side filtering by the AWS API and only returns the records that match the filter.

The `--output` argument is optional and is used to make the text easier to read.  `--output` values include `yaml`, `json`, `text`, and `table` 

A bad actor might run this command in several regions looking for running instances. Running this command in several regions increases the likelihood that FCS will score the ativity higher.  

The trick to getting a higher (more critical) score is to precede the “attack” with `DescribeSecurityGroups` or `DescribeInstances` and follow it with `DescribeInstances`.

## Get a Specific Security Group

Once a running instance has been found, get its security group.

```bash
aws --profile <profile-name> ec2 describe-instances \
--region <aws-region> \
--filters "Name=instance-state-name, Values=running" \
--max-items 1 \
--query "Reservations[].Instances[].SecurityGroups[].GroupId[]" \
--output json | jq -r '.[]'
```

This command is similar to the previous one.  

It uses the `--filter` arguement to do a server-side filter.  The `--query` arguement is a client-side filter.

`--max-items` returns only the first item.

The `--query` argument uses `json` to return the AWS security group id.  It has the prefix of `sg-`.

The `--output` is `json`.  This output gets piped ( `\` ) to `jq` and returns the security group id.

## Get Information About the Security Group

To raise the FCS score, use the AWS CLI to get information about the security group.

```bash
aws --profile <profile-name> ec2 describe-security-groups \
--region <aws-region> \
--group-id sg-################# \
--output yaml
```

Remember, IOAs are based on behavior.  While this command doesn't change an environment, it is something that a bad actor might do to get more information about an environment.

Similarly, this command returns the AWS meta-data tags attached to the security group.

aws --profile <profile-name> ec2 describe-tags \
--region <aws-region> \
--filters "Name=resource-id, Values=sg-#################" \
--output yaml

## Change the Security Group Rules to Allow Access from the Public Interenet

**WARNING**: This step changes the security group's inbound rules to give ports 80 and 3389 access to the public Internet.

**###### DO NOT DO THIS TO ANY TYPE OF PRODUCTION ENVIRONMENT ######**

```
oooooooooooo oooooo     oooo oooooooooooo ooooooooo.   
`888'     `8  `888.     .8'  `888'     `8 `888   `Y88. 
 888           `888.   .8'    888          888   .d88' 
 888oooo8       `888. .8'     888oooo8     888ooo88P'  
 888    "        `888.8'      888    "     888`88b.    
 888       o      `888'       888       o  888  `88b.  
o888ooooood8       `8'       o888ooooood8 o888o  o888o
```

Opening ports 80 and 3389 to production based environments is an RBE for most organizations.

RBE: _**Resume Building Event**_

```bash
aws --profile <profile-name> ec2 authorize-security-group-ingress \
--region <aws-region> \
--group-id sg-################# \
--protocol tcp \
--port 3389 \
--cidr 0.0.0.0/0
```

```bash
aws --profile <profile-name> ec2 authorize-security-group-ingress \
--region <aws-region> \
--group-id sg-################# \
--protocol tcp \
--port 22 \
--cidr 0.0.0.0/0
```

The `--cidr` address `0.0.0.0/0` is the public Internet.

## Change the Security Group Rules to DENY Access from the Public Internet

Revoke public access via this security group as quickly as possible.

Inside FCS/CSPM, public access to ports 80 and 3389 is also an IOM.  (Indicator of Misconfiguration) 

Depending on how often the assessments are run (every 2, 6, 12, or 24 hours), leave these ports open to see it inside FCS.  

Leaving these ports open, even for a short time, makes an environment vulnerable to attack/compromise.  Revoke access as quickly as possible.

```bash
aws --profile <profile-name> ec2 revoke-security-group-ingress \
--region <aws-region> \
--group-id sg-################# \
--protocol tcp \
--port 3389 \
--cidr 0.0.0.0/0
```

```bash
aws --profile <profile-name> ec2 revoke-security-group-ingress \
--region <aws-region> \
--group-id sg-################# \
--protocol tcp \
--port 22 \
--cidr 0.0.0.0/0
```

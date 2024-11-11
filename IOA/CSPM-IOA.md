# CLOUD-223: Trigger an IOA in AWS

Updated: 2024-11-11

**Objective**:

This document contains the steps needed to intentionally trigger an Indicator of Attack (IOA) in Falcon Cloud Security.

The "attack" portion of this exercise opens several ports in an EC2 security group. Two of them are management ports (22 and 3389) that generate Indicators of Misconfigurations (IOMs).

---
> 
> ⚠️ **Danger!**
>
> Some of these commands modify security settings.
>
> **Before you begin**, ensure you are authorized to make these changes in your environment.
>
> ☠️ **Proceed with caution.**
>
---

The IOA: **EC2 security group modified to allow ingress from the public internet**

The attack pattern includes:

- Performing reconnaissance (e.g., `ec2:DescribeSecurityGroups`, `ec2:DescribeInstances`)
- Modifying security groups (`ec2:AuthorizeSecurityGroupIngress`)
- Verifying the modifications (`ec2:DescribeSecurityGroups`)

## Prerequisites

1. **AWS Resources**

   - A running EC2 instance
   - AWS CLI version 2 installed

2. **Required IAM Permissions**

   - `ec2:DescribeInstances`: List EC2 instances
   - `ec2:DescribeSecurityGroups`: Retrieve security group details
   - `ec2:AuthorizeSecurityGroupIngress`: Add inbound rules
   - `ec2:RevokeSecurityGroupIngress`: Remove inbound rules

3. **Shell Variables**
   - `AWS_PROFILE`: AWS CLI profile
   - `AWS_REGION`: AWS region

### The AWS CLI

For information about the AWS CLI and how to download/configure it:

[https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Shell Variables

When creating shell variables, use the `export` keyword. This ensures variables are copied to any new shells spawned.

For example:

```shell
export AWS_REGION="us-east-1"
```

To verify the value of a shell variable, use the `echo` command and include a dollar sign (`$`) in front of the varible name.

```shell
echo $AWS_REGION
```

Alternatively, use the `env` command to list all current shell variables. Pipe the output through `sort` to make values easy to find.

```shell
env | sort
```

## Shell Commands

### Set Shell Variables

These commands set the `AWS_PROFILE` and `AWS_REGION` values for the session:

```shell
export AWS_PROFILE="cloud-223"
export AWS_REGION="ca-central-1"
```

When setting shell variables, quotation marks are _not_ required. However, using them can help prevent unexpected behavior.

### Initial Reconnisance

List the running instances in a region.

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --filters "Name=instance-state-name, Values=running" \
    --query 'Reservations[*].Instances[*].{
        Name: (Tags[?Key==`Name`] | [0].Value) || `No Name`,
        PublicIpAddress: PublicIpAddress,
        PrivateIpAddress: PrivateIpAddress,
        SecurityGroups: SecurityGroups[*].GroupId,
        InstanceId: InstanceId
    }' \
    --output yaml
```

This command retrieves a list of running EC2 instances in an AWS Region.

#### The `--filter` Parameter

`--filter` is a server-side directive that tells AWS to only return information from instances in a `running` state.

Other states (such as `stopped`, `terminated`, and `pending`) are excluded.

#### The `--query` Parameter

The `--query` parameter uses `JMESPath` syntax on the client-side to parse/select specific fields. It also formats the output.

- `Name`: Finds the instance tag with the key `Name` and displays its value. If no Name tag is set, it defaults to `No Name`.
- `PublicIpAddress`: Displays the public IP address of the instance, if available.
- `PrivateIpAddress`: Shows the private IP address of the instance.
- `SecurityGroups`: Lists the security group IDs associated with the instance.

The command `aws ec2 describe-instances` returns a JSON object that includes a list of `Reservations` and `Instances`.

EC2 `Reservations` primarily refer to cost and commitment structures. The main types are on-demand, reserved, savings plans, spot, dedicated, and capacity.

Within each `Reservation` is an `Instances` array. This array contains information about each EC2 instance with the reservation.

`Reservations[*].Instances[*]` returns a list of all the reservations and instances.

There are multiple ways to limit the output to a single instance. In this example, replace the asterisks (`*`) in `Reservations` and `Instances` with the number `0`.

> **Note**: The AWS CLI has a parameter `--max-items` that should limit the output to a single entry.  However, in this case, it won't work as expected. 
> 
> This is because the `--max-items` flag applies to the *number of items* returned by the command *at the top level* and **not** individual responses within reservations. 
>  
>  Using `--max-items 1` does return a single item.  When the command has *multiple* top-level matches, they are returned even when `null`.  The extra lines interfere with the following step that assigns the value to a shell variable.
> 
> Choosing the first value of the array is safer.

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --filters "Name=instance-state-name, Values=running" \
    --query 'Reservations[0].Instances[0].{
        Name: (Tags[?Key==`Name`] | [0].Value) || `No Name`,
        PublicIpAddress: PublicIpAddress,
        PrivateIpAddress: PrivateIpAddress,
        SecurityGroups: SecurityGroups[*].GroupId,
        InstanceId: InstanceId
    }' \
    --output yaml
```

AWS does **not** guarantee the order of data. When there are multiple EC2 instances in an array, it is possible the output order will change every time the command runs.

To address this, put the Instance ID in a shell variable.

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --filters "Name=instance-state-name, Values=running" \
    --query 'Reservations[0].Instances[0].InstanceId' \
    --output text
```

To minimize copy/paste errors, assign the value directly using this command.

```shell
export INSTANCE_ID=$(aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --filters "Name=instance-state-name, Values=running" \
    --query 'Reservations[0].Instances[0].InstanceId' \
    --output text)
```

---

> [!Note] **CLI: Pro-Tip**
> 
> The linux `history` feature has a shortcut that repeats the last command. The shortcut is: `!!`
> 
>  At the command line, type `!!` and press enter.  The previous command will reappear.
>  
> If this was the last command typed:
> 
> ```shell
> aws ec2 describe-instances \
>   --profile $AWS_PROFILE \
>   --region $AWS_REGION \
>   --filters "Name=instance-state-name, Values=running" \
>   --query 'Reservations[0].Instances[0].InstanceId' \
>   --output text
>   ```
> 
  >  Use `!!` to set a shell variable:
>  
>  ```shell
>  export INSTANCE_ID=$(!!)
>  ```
>  
>  _It looks like laziness but, in reality, it is efficiency!_

---

Verify the value of INSTANCE_ID: 

```shell
echo $INSTANCE_ID`
```

### Get the Security Group ID

This command returns a list of security groups attached to the EC2 instance.

The `--query` parameter includes formatting to make the output clear.

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --instance-id $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].{
        SecurityGroups: SecurityGroups[*].GroupId
        }' \
    --output yaml
```

For this exercise, only one security group is needed.

Update the `--query` parameter to select the first (possibly only) security group by replacing the asterisk (`*`) in `SecurityGroups` with a `0`.

Remove the formatting too.

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --instance-id $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
    --output text
```

### Assign the Security Group ID to a Shell Variable

Either use the `!!` trick or copy/paste the command into a variable assignment statement.

```shell
export AWS_SG_ID=$(aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --instance-id $INSTANCE_ID \
    --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId' \
    --output text)
```

### Check the Existing Security Group Rules

To get information about security groups, use `describe-security-groups`.

This example displays information about inbound (ingress) traffic for the AWS security group saved in `AWS_SG_ID`.

The output includes port information, protocols, and sources.

```shell
aws ec2 describe-security-groups \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-ids $AWS_SG_ID \
    --query 'SecurityGroups[*].{
        GroupId: GroupId,
        InboundRules: IpPermissions[*].{
            Port: ToPort,
            Protocol: IpProtocol,
            Source: join(`, `, [IpRanges[].CidrIp, UserIdGroupPairs[].GroupId][])
        }
    }' \
    --output yaml
```

The `--query` paramater use `JMESPATH` to parse/format the output.

- `GroupId`: Returns the security group ID.
- `InboundRules`: An array of the security group’s inbound rules.

For each inbound rule, it displays:

- `Port`: The destination port number allowed by this rule (`ToPort`).
- `Protocol`: The IP protocol for the rule (`IpProtocol`), like `TCP` or `UDP`.
- `Source`: The allowed source IP ranges or security group IDs.

The `Source` field uses a `join` function to combine:

- `IpRanges[].CidrIp`: The CIDR IP ranges allowed by this rule.
- `UserIdGroupPairs[].GroupId`: Other security groups allowed by this rule.

### Modify the Security Group

This is the actual "attack."

These commands open specific ports to all IP addresses, which will trigger an Indicator of Attack (IOA).

---

> [!Caution]
> 
> These security group modifications allow ☢️ **unrestricted access** ☢️ to the public Internet.
>  
>  After testing, revert these settings as quickly as possible.

---

When the command is successful, this is part of the output: `Return: true`.

#### Allow SSH (Port 22)

```shell
aws ec2 authorize-security-group-ingress \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-id $AWS_SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

#### Allow RDP (Port 3389)

```shell
aws ec2 authorize-security-group-ingress \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-id $AWS_SG_ID \
    --protocol tcp \
    --port 3389 \
    --cidr 0.0.0.0/0
```

#### Optional: Allow a Random Port

As a test, pick a random port number. For example, use the current four-digit year or the current date.

```shell
aws ec2 authorize-security-group-ingress \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-id $AWS_SG_ID \
    --protocol tcp \
    --port 1108 \
    --cidr 0.0.0.0/0
```

### Verify the Changes

Use the `describe-security-groups` to display the security group's inbound rules.

```shell
aws ec2 describe-security-groups \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-ids $AWS_SG_ID \
    --query 'SecurityGroups[*].{
        GroupId: GroupId,
        InboundRules: IpPermissions[*].{
            Port: ToPort,
            Protocol: IpProtocol,
            Source: join(`, `, [IpRanges[].CidrIp, UserIdGroupPairs[].GroupId][])
        }
    }' \
    --output yaml
```

### Optional: View all EC2 instances that use this Security Group

As a bit of _bonus_ reconnaissance, this command displays all EC2 instances using that security group.

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --filters "Name=instance.group-id,Values=$AWS_SG_ID" \
    --query 'Reservations[*].Instances[*].InstanceId' \
    --output text
```

Here's the same command with more details about the instance(s).

```shell
aws ec2 describe-instances \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --filters "Name=instance.group-id,Values=$AWS_SG_ID" \
    --query 'Reservations[*].Instances[*].{
        Name: (Tags[?Key==`Name`] | [0].Value) || `No Name`,
        PublicIpAddress: PublicIpAddress,
        PrivateIpAddress: PrivateIpAddress,
        SecurityGroups: SecurityGroups[*].GroupId,
        InstanceId: InstanceId
    }' \
    --output yaml
```

### Revert Security Group Changes

These commands revoke the access granted in the previous steps and restores the security group’s original settings.

The AWS CLI command is: `revoke-security-group-ingress`

#### Revoke SSH: Port 22

```shell
aws ec2 revoke-security-group-ingress \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-id $AWS_SG_ID \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0
```

#### Revoke RDP: Port 3389

```shell
aws ec2 revoke-security-group-ingress \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-id $AWS_SG_ID \
    --protocol tcp \
    --port 3389 \
    --cidr 0.0.0.0/0
```

#### Revoke Random/Optional Port

```shell
aws ec2 revoke-security-group-ingress \
    --profile $AWS_PROFILE \
    --region $AWS_REGION \
    --group-id $AWS_SG_ID \
    --protocol tcp \
    --port 1108 \
    --cidr 0.0.0.0/0
```

As with the authorize command, when successful, the output contains: `Return: true`.


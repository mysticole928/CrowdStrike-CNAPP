# Notes on the Falcon KAC

Updated: 2024-10-21

The Falcon Kubernetes Admission Controller, evaluates container-based configurations and sends telemetry to the Falcon console.

The notes in this directory cover some of use-cases I've found during deployments.

The CLI-Output-Script folder has a shell script that I wrote that processes KAC warning messages from the linux command line when deploying containers.  It's a work in progress and there are a couple of bugs I need to work out.

`IMDSv2.md` addesses issues that arise when using the Falcon KAC with EC2 instances with IMDSv2 turned on.  IMDSv2 encrypts the metadata on the instance including the `Name` tag.  The KAC's functionality is *not* impacted.  However, the cluster name will not appear in the Host Managemen console.  If there are Host Group assingments made using the name of the cluster, they will not run.  There are two ways to address this; assign a sensor grouping tag using `Helm` or update the config map for the KAC and restart the pod.

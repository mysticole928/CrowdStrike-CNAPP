# KAC Check-in Information
Author: Stephen Cole
Date: 2024-12-16

This short query is useful for verifying the Kubernetes Admission Controller (KAC) connection with Falcon Cloud Security.

## This CQL query diplays three columns:

- The Kubernetes Cluster Name
- The KAC AID
- The timestamp from the most recent check-in with FCS

```
#event_simpleName = K8SClusterInfo 
| aid = * 
| sort(K8SClusterName, order=asc)
| groupBy([K8SClusterName, aid, aid_timestamp], 
    function=[
        { 
            max(@timestamp, as=latest_timestamp) 
            | aid_timestamp := formatTime("%Y-%m-%d %H:%M:%S", field=latest_timestamp) 
            | drop(latest_timestamp)
        }    
    ]
  )
```

The function embedded in the `groupBy()` statement returns the most recent check-in timestamp.  

- It gets the most recent check-in and assigns the value to `latest_timestamp`.
- It formats `latest_timestamp` to make it human readable and assigns it to the variable `aid_timestamp`.  
- The temporary value `latest_timestamp` is dropped.

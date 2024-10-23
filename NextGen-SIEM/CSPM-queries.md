# CrowdStrike Query Language Queries for CSPM

## Find All Policy Violations with NIST Benchmark Information

This simple query lists default (CrowdStrike provided) CSPM policy violations that contain NIST benchmarks.

```
"#event_simpleName"=~/^cspm_policy_\d+/
	| "nist_benchmark_ids" = * 
  | !in(field=nist_benchmark_ids, values=[null, ""])
  | nist_benchmark_ids = /^\{(?<ids>.+)}/
  | splitString(by=",", field=ids, as=nist_ids)
	| groupBy([CloudPlatform, PolicyId, policy_severity, PolicyStatement, nist_benchmark_ids], function=collect(ResourceId))
	| sort([policy_severity,PolicyID], order=[desc, asc], limit=20000) 
```

The `#event_simpleName` query uses regex.  Specifying a number using `\d+` instead of the `*` ensures the query is efficient.

## Search AWS for Instances with Public IP Addresses

```
"aws_public_ip_address"= * and not "aws_public_ip_address" = "null"
| groupBy([aws_instance_name,aws_public_dns_name, aws_public_ip_address, aws_region], function=collect(aws_region))
```

The `and not "aws_public_ip_address" = "null"` avoids false positives where `null` is the value.

## Query a Custom CSPM Policy

This is an example of a search for custom CSPM policy and will not work without modification.  

The custom policy is attached to IAM and its rules fairly simple.  It searches for users with an active secret key (API access) that has been used at least once.

```
#event_simpleName = "custom_detection_policy" 
| policy_id = "1001"
| sort(ResourceId, order=asc) 
| parseJson(ResourceAttributes, prefix=ResourceAttributes.)
| parseTimestamp(field="ResourceAttributes.Access Key 1 Last Rotated", as="ResourceAttributes.Access Key 1 Last Rotated.timestamp", timezoneAs="ResourceAttributes.Access Key 1 Last Rotated.timezone")
| keyTimestamp := getField("ResourceAttributes.Access Key 1 Last Rotated.timestamp")
| keyAge := now() - keyTimestamp
| keyAgeInDays := formatDuration("keyAge", precision=2)
| groupBy([policy_id, policy_statement, service, region, ResourceId, keyAgeInDays])
```

In the data is a field called `ResourceAttributes`.  It's formatted as in-line `JSON`.  

The statement `parseJson(ResourceAttributes, prefix=ResourceAttributes.)` extracts the in-line `JSON` data as fields for the query.  

The fields get the prefix: `ResourceAttributes.`

These data is used to calculate the age the key and display it in the results.



# Get Falcon KAC Version Information

Use `kubectl` to verify the version of the Falcon KAC.

## Using `kubectl` with `jsonpath` to filter output

```
kubectl get pods -n falcon-kac \
-o jsonpath='{range .items[*]}{"\n"}{.metadata.name}{"\n"}{range .spec.containers[*]}{"\n"}{"  - "}{.image}{end}{end}{"\n"}'
```

The output:

```
falcon-kac-f796fcb66-577xr

  - 000000000000.dkr.ecr.us-east-7.amazonaws.com/falcon-kac:7.18.0-1603.container.x86_64.Release.US-1
  - 000000000000.dkr.ecr.us-east-7.amazonaws.com/falcon-kac:7.18.0-1603.container.x86_64.Release.US-1

```

The output includes the container registry information, the repository, and the tag.

## Using `kubectl` and `jq` to filter output

Pipe the output from `kubectl` through `jq` to get only the respostory name and the tag.

```
kubectl get pods -n falcon-kac \
-o jsonpath='{range .items[*]}{"\n"}{.metadata.name}{"\n"}{range .spec.containers[*]}{"\n"}{"  - "}{.image}{end}{end}{"\n"}' | \
jq -R -r 'if test("^[^ ]") then . + "\n" else capture("/(?<repository>[^/]+):(?<tag>.+)") | "  - \(.repository):\(.tag)" end'
```

In `jq` the `-R` option specifies raw JSON.  The `-r` option is for raw output.  If the `-r` is ommited, each line will have quotation marks.

The `test()` statement ignores every line except the one with container information.

The `capture()` statement uses `regex` to parse the lines with container information and creates variables for the repository and tag.

The output:

```
falcon-kac-64878c4fdf-tzzws
  - falcon-kac:7.20.0-1807.container.x86_64.Release.US-1
  - falcon-kac:7.20.0-1807.container.x86_64.Release.US-1
  - falcon-kac:7.20.0-1807.container.x86_64.Release.US-1
```


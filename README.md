# Prometheus Metric Checker

This script will run some simple Prometheus queries against a configured host for
use by Asserts to verify whether metrics structure is compatible with an Asserts installation.

## Requirements

* A prometheus url to connect to and query
* A container runtime or k8s cluster if using the provided container image  
* [Python Poetry](https://python-poetry.org/) installed for running in non containerized environments

## Running the script

### Docker

```sh
docker run -it -e PROMETHEUS_HOST=http://prometheus-host.example.com asserts/qualifier:latest
```

Which will print the results to stdout.

### K8s

`cd deploy` open the file `job.yaml` and change `--host` value to the appropriate url.

```shell
kubectl apply -f job.yaml
```

Retrieve output with:

```shell
POD=$(kubectl get pods -l job-name=qualifier --output=jsonpath='{.items[*].metadata.name}')
kubectl logs $POD
```

### Locally

```shell
poetry shell
poetry install
python cli.py --host http://prometheus-host.example.com
```

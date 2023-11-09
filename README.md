This repository contains a test application built to investigate how CPU requests and limits can affect application performance and end to end latency. It also contains suggestions on what metrics are available in the different layers (`kubelet`, `containerd`, etc.) to prevent, identify and debug this type of issues.

# Getting started

* Deploy the `loadsvc` applications:

```
kubectl apply -f ./deploy/none/sync.yaml && kubectl apply -f ./deploy/none/async.yaml
```

* Deploy the `webapp` application:

```
kubectl apply -f ./deploy/none/webapp.yaml
```

* Port-forward the `webapp` port:

```
kubectl port-forward deployment/webapp 8282
```

* Generate some load (defaults to 2 CPUs per `loadsvc` service, during 60 seconds):

```
curl http://localhost:8282/do_work
```

## (Optional) Deploy the Datadog Agent

The applications are already instrumented for APM with Datadog. To get metrics, traces, and logs into Datadog, follow the instructions below:

* Deploy the Datadog Operator:

```
helm repo add datadog https://helm.datadoghq.com
helm install my-datadog-operator datadog/datadog-operator
```

* Create a secret with your Datadog credentials:

```
kubectl create secret generic datadog-secret --from-literal=api-key=<YOUR_DD_API_KEY> --from-literal=app-key=<YOUR_DD_APP_KEY>
```

* Deploy the Datadog Agent:

```
kubectl apply -f ./deploy/none/datadog.yaml
```

# Architecture

The application has a main web service, `webapp`, that calls two micro-services that generate CPU load. One is called synchronously, the other asynchronously (fire & forget).

![Architecture diagram](./static/architecture.jpg)

## `webapp`

The main web service, `webapp`, exposes a couple of endpoints:

 * `/`: Just a test endpoint, returns "Hello, world!"
 * `/do_work`: The main endpoint, which launches a call to the `sync` service, to the `async` service, or both. It has several parameters:
   * `type`: the type of service to call. Potential values: `async`, `sync`, `both`. Default: `both`.
   * `ncpus_sync`: the number of CPUs to stress in the `sync` service. Default: 2.
   * `ncpus_async`: the number of CPUs to stress in the `async` service. Default: 2.
   * `timeout_sync`: the time in seconds to stress the CPUs in the `sync` service. Default: 60.
   * `timeout_async`: the time in seconds to stress the CPUs in the `async` service. Default: 60.

## `loadsvc`

The `loadsvc` micro-service is the web service that gets deployed both as the `sync` and the `async` services. `loadsvc` uses [stress-ng](https://github.com/ColinIanKing/stress-ng) to generate CPU load. As `stress-ng` states in their [README](https://github.com/ColinIanKing/stress-ng/blob/master/README.md), it has to be used with caution, as some of the tests can make a system run hot on poorly designed hardware and also can cause excessive system thrashing which may be difficult to stop. `loadsvc` uses only a very small set of `stress-ng`'s features, so it should be pretty safe to run.

It exposes two endpoints:

 * `/`: Test endpoint, returns the number of CPUs in the node where the pod is deployed
 * `/load`: The main endpoint, which launches `stress-ng`. It has a couple of parameters:
   * `ncpus`: the number of CPUs to stress. Default: 2.
   * `timeout`: the time in seconds to stress the CPUs. Default: 60.
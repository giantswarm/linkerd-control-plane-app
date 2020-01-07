[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

# linkerd2-app chart

This chart is based on the official linkerd2 helm chart. The main difference it offers is a
direct integration with [cert-manager](https://cert-manager.io/) used to generate certificates
for linkerd2 components.

The chart is currently based on the "edge" release of linkerd2, as it supports loading certificates
from `cert-manager` prepared secrets.

## Requirements

- you can install only one release of this chart per kubernetes cluster

## Installation

### Dependencies

This application requires the [`cert-manager`](https://github.com/giantswarm/cert-manager-app)
application to be already deployed in the cluster. You can install it with the following command:

```bash
helm install --namespace kube-system -n cert-manager --version=1.0.1 giantswarm/cert-manager-app
```

### Deployment

When `cert-manager` is ready, you can install linkerd2 with the command below. Please note that
we have to pass `-set Identity.Issuer.Scheme='linkerd.io/cert-manager` to make the chart use
`cert-manager`. Also, for compatibility with upstream chart, please note that we need to specify the namespace
to install to twice: first in the `--namespace` parameter of helm, then as `--set Namespace` parameter
of the chart. Recommended namespace name is `linkerd`, which is already included below:

```text
helm install --namespace linkerd -n linkerd giantswarm-playground-catalog/linkerd2 --set Identity.Issuer.Scheme='linkerd.io/cert-manager' --set Namespace=linkerd
```

## Configuration

Two installation options, `Identity.Issuer.Scheme` and `Namespace` are required to install this chart,
as shown above. You shouldn't need to change other defaults. Still, you can check available chart
options [here](helm/linkerd2-app/values.yaml).

## Compatibility

Tested on Giant Swarm release 10.1.0 on AWS with Kubernetes 1.15.5.

## Credit

* https://helm.linkerd.io/stable

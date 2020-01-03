[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

# linkerd2-app chart

This chart is based on the official linkerd2 helm chart. The main difference it offers is a
direct integration with [cert-manager](https://cert-manager.io/) used to generate certificates
for linkerd2 components.

The chart is currently based on the "edge" release of linkerd2, as it supports loading certificates
from `cert-manager` prepared secrets.

## Requirements

- you should install only one release of this chart per kubernetes cluster

## Installation

### Dependencies

This application requires the [`cert-manager`](https://github.com/giantswarm/cert-manager-app)
application to be already deployed in the cluster. You can install it with the following command:

```bash
helm install -n cert-manager giantswarm-default-catalog/cert-manager-app
```

### Deployment

When `cert-manager` is ready, you can install linkerd2 with the command below. Please note that
we have to pass `-set Identity.Issuer.Scheme='linkerd.io/cert-manager` to make the chart use
`cert-manager`.

```text
helm install -n linkerd2 giantswarm-playground-catalog/linkerd2 --set Identity.Issuer.Scheme='linkerd.io/cert-manager'
```

## Configuration

You shouldn't need to change the defaults. Still, you can check available chart options [here](helm/link/../linkerd2-app/values.yaml).

## Compatibility

Tested on Giant Swarm release 9.0.0 on AWS with Kubernetes 1.15.5.

## Credit

* https://helm.linkerd.io/stable

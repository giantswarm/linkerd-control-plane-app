[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

# linkerd2-app chart

This chart is based on the official linkerd2 helm chart. The main difference it offers is a
direct integration with [cert-manager](https://cert-manager.io/) used to generate short-lived
certificates for linkerd2 components. This results in an entirely hands-off install - no
need to generate a CA certificate prior to installation.

## Requirements

- you can install only one release of this chart per kubernetes cluster.
- `cert-manager` must already be deployed in the cluster.
- it is strongly suggested to use the [`linkerd2-cni-app`](https://github.com/giantswarm/linkerd2-cni-app) as this results in a more secure setup.
  - the CNI must be installed before this chart, and `global.cniEnabled: true` must be set.

## Installation

### Dependencies

This application requires the [`cert-manager`](https://github.com/giantswarm/cert-manager-app)
application to be already deployed in the cluster. This can be installed from the Giant Swarm
App Catalog via the Happa UI.

### Deployment

When `cert-manager` is ready, you can install Linkerd2 with the command below. Note that integration
with cert-manager is enabled by default and you don't need to do anything to configure this. If you
wish to use certificates provided from elsewhere, you must set `global.identity.issuer.scheme: linkerd.io/tls`
and also provide the required certificates via the values file.

This chart diverges from the upstream chart slightly by taking the namespace value from Helm
directly, rather than from the values file. This means the namespace must be created _before_
this chart is deployed. Assuming a namespace `linkerd` already exists, this chart can be
deployed with the following command:

```text
helm install --namespace linkerd -n linkerd giantswarm-playground-catalog/linkerd2-app
```

## Configuration

If you are deploying this chart on top of Linkerd's CNI driver then you must enable this
behaviour by setting `global.cniEnabled: true`.

### Note:

`values.yaml` uses [YAML anchors](https://helm.sh/docs/chart_template_guide/yaml_techniques/#yaml-anchors) to
be DRY where possible, however this can cause problems when these values are overridden by a custom
values file. If you wish to enabled or disable deployment of the `grafana` and `tracing` subcharts
then you should override the values at `.$subchart.enabled`, **not** `.global.$subchart.enabled`.

## Compatibility

Tested on Giant Swarm release 10.1.0 on AWS with Kubernetes 1.15.5.

## Credit

* https://helm.linkerd.io/stable

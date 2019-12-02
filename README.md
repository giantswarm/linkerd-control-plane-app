[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

# linkerd2-app chart

Giant Swarm offers a linkerd2 Managed App which can be installed in tenant clusters.
Here we define the linkerd2 chart with its templates and default configuration.

Currently based on "edge" release of linkerd2.

## Usage

This application requires the [`cert-manager`](https://github.com/giantswarm/cert-manager-app)
application to be already deployed in the cluster, like:

```bash
helm install -n cert-manager giantswarm-default-catalog/cert-manager-app
```

You need to pass at least the following parameter to use `cert-manager` mode:

```text
helm install -n linkerd2 giantswarm-playground-catalog/linkerd2 --set Identity.Issuer.Scheme='linkerd.io/cert-manager'
```

## Credit

* https://helm.linkerd.io/stable


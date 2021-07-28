[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

# linkerd2-app chart

Linkerd2 service mesh for Giant Swarm clusters. Although based on the official linkerd2 helm chart,
it diverges in few places to ease installation on Giant Swarm clusters.

**Before you install this app, please review this document thoroughly!**

## Requirements

- You can install only one release of this chart per kubernetes cluster.
- The only possible namespace name you can install into is `linkerd`.
- Default installation values require the installation of [`linkerd2-cni-app`](https://github.com/giantswarm/linkerd2-cni-app) before installing this app.
  - the CNI must be installed before this chart, and `cniEnabled: true` must be set (default).
- With linkerd CNI enabled, all of your workload pods meshed by linkerd require a `PodSecurityPolicy` which allows use of `EmptyDir` volumes.
  - the injected linkerd-proxy container and proxy initContainer require an `EmptyDir` volume to store ephemeral information.
- (Optional but recommended). The [`linkerd` cli tool](https://github.com/linkerd/linkerd2/releases/tag/stable-2.10.2) is very useful to verify your installation working and for installation of additional extensions. Make sure you [set the right flags](#usage-with-linkerd-cli)

## Configuration

Please review the [default values.yaml file](helm/linkerd2-app/values.yaml) and change
the defaults by specifying a [user configuration](https://docs.giantswarm.io/app-platform/app-configuration/).

With the default values, linkerd will be installed in High-Availability mode and with CNI plugin enabled.

If you're planning to install this chart without the CNI plugin,
you'll need to set `cniEnabled: false` in your values file

A successful install will require you to generate a trust anchor and issuer certificate. The following steps loosely follow [the official instructions](https://linkerd.io/2.10/tasks/generate-certificates/).

Obtain the `step` cli (we're using `step_linux_0.16.1_amd64.tar.gz` from [here](https://github.com/smallstep/cli/releases/tag/v0.16.1)) and execute the following commands. Take note of the `--not-after` flag. (8760h = 1 year)

```
step certificate create root.linkerd.cluster.local ca.crt ca.key --profile root-ca --no-password --insecure --not-after=8760h
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key --profile intermediate-ca --not-after=8760h --no-password --insecure --ca ca.crt --ca-key ca.key
expiry=$(openssl x509 -in issuer.crt -noout -enddate)
expiry_iso=$(date -Iseconds --utc --date "${expiry#notAfter=}")
echo "${expiry_iso%+00:00}Z"
```

Finally construct your config file like this:

```
identity:
  issuer:
    crtExpiry: <the final output of the commands above>
    tls:
      crtPEM: |
        <contents of the issuer.crt file>
      keyPEM: |
        <contents of the issuer.key file>
identityTrustAnchorsPEM: |
  <contents of the ca.crt file>
```

### Note:

`values.yaml` uses [YAML anchors](https://helm.sh/docs/chart_template_guide/yaml_techniques/#yaml-anchors) to
be DRY where possible.

## Installation

### Dependencies

This application requires the [`linkerd2-cni-app`](https://github.com/giantswarm/linkerd2-cni-app)
application to be already deployed in the cluster. It can be installed from the Giant Swarm
App Catalog through an `AppCR` (recommended) or via the Web UI (additional [labels/annotations required](https://github.com/giantswarm/linkerd2-cni-app#installation)).

### Deployment

This chart diverges from the upstream chart slightly by taking the namespace value from Helm
directly, rather than from the values file. When installing through the Giant Swarm App platform, we recommend
to install via App CR. Make sure you set the required annotations and labels through the `spec.namespaceConfig`.

```yaml
...
  namespaceConfig:
    annotations:
      linkerd.io/inject: disabled
    labels:
      linkerd.io/is-control-plane: "true"
      config.linkerd.io/admission-webhooks: disabled
      linkerd.io/control-plane-ns: linkerd
...
```

#### Deployment using helm

When using helm, the namespace must be created _before_
this chart is deployed. Assuming a namespace `linkerd` already exists, this chart can be
deployed with the following command:

```text
helm install --namespace linkerd -n linkerd giantswarm-playground-catalog/linkerd2-app
```

Make sure to add the neccessary annotations and labels to your namespace. Check out file [helm/linkerd2-app/templates/namespace.yaml](helm/linkerd2-app/templates/namespace.yaml) as example.

### After deployment

After you've installed the app, linkerd requires some labels and annotations on the `kube-system` namespace to disable proxy injection for pods running there.

```bash
kubectl annotate namespace kube-system linkerd.io/inject=disabled
kubectl label namespace kube-system config.linkerd.io/admission-webhooks=disabled
```

We strongly recommend installing the `linkerd viz` extension using the [`linkerd`](#usage-with-linkerd-cli) by executing

```bash
linkerd viz install | kubectl apply -f -
```

After installation, you can open the dashboard by executing

```
linkerd viz dashboard
```

## Usage with `linkerd` cli

You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.10.2).

## Credit

* https://linkerd.io/2.10/tasks/install-helm/

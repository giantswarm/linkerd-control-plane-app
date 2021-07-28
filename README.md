[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

# linkerd2-app chart

Linkerd2 service mesh for Giant Swarm clusters. Based on the official linkerd2 helm charts with a few changes, required to deploy to Giant Swarm clusters.

**Before you install this app, please review this document from start to finish!**

## Quickstart Guide

### Step 1: Pre-installation and Configuration

- Install the linkerd CNI plugin by installing [`linkerd2-cni-app`](https://github.com/giantswarm/linkerd2-cni-app) on your cluster. Be sure to review the instructions for the CNI plugin.
- A successful install will require you to generate a trust anchor and issuer certificate. The following steps loosely follow [the official instructions](https://linkerd.io/2.10/tasks/generate-certificates/).

Obtain the `step` cli (we're using `step_linux_0.16.1_amd64.tar.gz` from [here](https://github.com/smallstep/cli/releases/tag/v0.16.1)) and execute the following commands. Take note of the `--not-after` flag. (8760h = 1 year)

```
step certificate create root.linkerd.cluster.local ca.crt ca.key --profile root-ca --no-password --insecure --not-after=8760h
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key --profile intermediate-ca --not-after=8760h --no-password --insecure --ca ca.crt --ca-key ca.key
expiry=$(openssl x509 -in issuer.crt -noout -enddate)
expiry_iso=$(date -Iseconds --utc --date "${expiry#notAfter=}")
echo "${expiry_iso%+00:00}Z"
```

- Finally construct your user secrets file like this:

```yaml
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

- Review the [default values.yaml file](helm/linkerd2-app/values.yaml) and change
other defaults by specifying a [user configuration](https://docs.giantswarm.io/app-platform/app-configuration/). With the default values, linkerd will be installed in High-Availability mode and with CNI plugin enabled.

### Step 2: Deploy Linkerd

We recommend deploying the app by applying an `App` CR (Custom Resource) onto your management cluster. You can use the [`kubectl gs`](https://docs.giantswarm.io/ui-api/kubectl-gs/) plugin to generate a valid `App` CR with command

```
kubectl gs template app \
  --catalog giantswarm \
  --name linkerd2-app \
  --namespace linkerd \
  --cluster <your-cluster-id>  \
  --version 0.6.0 \
  --user-configmap my-linkerd-values.yaml \
  --user-secrets my-linkerd-certificates.yaml
```

**Attention**: You'll need to edit the resulting `App` CR manifest to add `spec.namespaceConfig.labels` and `spec.namespaceConfig.annotations` fields.

The final `App` CR should look like this:

```yaml
apiVersion: application.giantswarm.io/v1alpha1
kind: App
metadata:
  name: linkerd2-app
  namespace: <your-cluster-id>
spec:
  catalog: giantswarm
  kubeConfig:
    inCluster: false
  name: linkerd2-app
  namespace: linkerd
  namespaceConfig:
    annotations:
      linkerd.io/inject: disabled
    labels:
      linkerd.io/is-control-plane: "true"
      config.linkerd.io/admission-webhooks: disabled
      linkerd.io/control-plane-ns: linkerd
  userConfig:
    configMap:
      name: linkerd2-app-userconfig
      namespace: <your-cluster-id>
    secret:
      name: linkerd2-app-userconfig
      namespace: <your-cluster-id>
  version: 0.6.0

```

When installing via the Giant Swarm web UI, you'll need to apply the above labels and annotations manually.

### Step 4: After deployment

- Disable proxy injections for pods running in the `kube-system` namespace by applying certain labels and annotations

```bash
kubectl annotate namespace kube-system linkerd.io/inject=disabled
kubectl label namespace kube-system config.linkerd.io/admission-webhooks=disabled
```

- Optional but recommended: You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.10.2).

- We strongly recommend installing the `linkerd viz` extension using the [`linkerd`](#usage-with-linkerd-cli) by executing

```bash
linkerd viz install | kubectl apply -f -
```

After installation, you can open the dashboard by executing

```
linkerd viz dashboard
```

## Mesh your workloads

After installation, linkerd looks for a `linkerd.io/inject: enabled` annotation on `Namespaces` or other workload resources. Adding this annotation to your workload namespaces will trigger automatic proxy container injection to your pods. More information on proxy injection can be found on the ["Automatic Proxy Injection" page](https://linkerd.io/2.10/features/proxy-injection/) in the upstream documentation.

**Attention**: Proxy containers are using `EmptyDir` volumes for storing ephemeral data, so all of your workload pods meshed by linkerd require a `PodSecurityPolicy` which allows use of `EmptyDir` volumes.

## Installing without the CNI plugin

In order to install this app without the CNI plugin, you'll need to specify `cniEnabled: false` in your user configuration.

Be aware that running without the CNI plugin, proxy containers will run as `root` and will require `NET_ADMIN` and `NET_RAW` capabilities.

## Troubleshooting

### App installation fails when I specify a namespace name other than `linkerd`

The `linkerd` namespace name is assumed in several parts of the chart, so we restricted installation to namespaces named `linkerd` only.

### Proxy containers fail to start

Your workload must be able to create `EmptyDir` volumes, so you'll need to create a `PodSecurityPolicy` allowing the creation of `EmptyDir` volumes.

## Usage with `linkerd` cli

You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.10.2).

## Credit

* https://linkerd.io/2.10/tasks/install-helm/

# linkerd2-app chart

[![CircleCI](https://circleci.com/gh/giantswarm/linkerd2-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd2-app)

Linkerd2 service mesh for Giant Swarm clusters. Based on the official linkerd2 helm charts with a few changes, required to deploy to Giant Swarm clusters.

**Before you install this app, please review this document from start to finish!**

## Quickstart Guide

### Step 1: Pre-installation and Configuration

- Install the linkerd CNI plugin by installing [`linkerd2-cni-app`](https://github.com/giantswarm/linkerd2-cni-app) on your cluster. Be sure to review the instructions for the CNI plugin.
- A successful install will require you to generate a trust anchor and issuer certificate. The following steps loosely follow [the official instructions](https://linkerd.io/2.10/tasks/generate-certificates/).

Obtain the `step` cli (we're using `step_linux_0.16.1_amd64.tar.gz` from [here](https://github.com/smallstep/cli/releases/tag/v0.16.1)) and execute the following commands. Take note of the `--not-after` flag. (8760h = 1 year)

```bash
step certificate create root.linkerd.cluster.local ca.crt ca.key --profile root-ca --no-password --insecure --not-after=8760h
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key --profile intermediate-ca --not-after=8760h --no-password --insecure --ca ca.crt --ca-key ca.key
expiry=$(openssl x509 -in issuer.crt -noout -enddate)
expiry_iso=$(date -Iseconds --utc --date "${expiry#notAfter=}")
echo "${expiry_iso%+00:00}Z"
```

- Finally construct your user secrets file by filling this template and saving as `my-linkerd-certificates.yaml`:

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

- Download the [default values.yaml file](helm/linkerd2-app/values.yaml) and save it as `my-linkerd-values.yaml` to create a [user configuration](https://docs.giantswarm.io/app-platform/app-configuration/). Review the values in the file. With the default values, linkerd will be installed in High-Availability mode and with CNI plugin enabled.

### Step 2: Deploy Linkerd

We recommend deploying the app by applying an `App` CR (Custom Resource) onto your management cluster. Use the [`kubectl gs`](https://docs.giantswarm.io/ui-api/kubectl-gs/) plugin to generate a valid `App` CR with command:

```bash
kubectl gs template app \
  --catalog giantswarm \
  --name linkerd2-app \
  --namespace linkerd \
  --cluster <your-cluster-id>  \
  --version 0.6.0 \
  --user-configmap my-linkerd-values.yaml \
  --user-secret my-linkerd-certificates.yaml \
  --namespace-labels "linkerd.io/is-control-plane=true,config.linkerd.io/admission-webhooks=disabled,linkerd.io/control-plane-ns=linkerd" \
  --namespace-annotations "linkerd.io/inject=disabled" > linkerd-manifest.yaml
```

The final `App` CR should look like this:

```yaml
...
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
      config.linkerd.io/admission-webhooks: disabled
      linkerd.io/control-plane-ns: linkerd
      linkerd.io/is-control-plane: "true"
  userConfig:
    configMap:
      name: linkerd2-app-userconfig-<your-cluster-id>
      namespace: <your-cluster-id>
    secret:
      name: linkerd2-app-userconfig-<your-cluster-id>
      namespace: <your-cluster-id>
  version: 0.6.0
```

Please note, that for security reasons Giant Swarm by default forbids the usage of
`emptyDir` volumes as storage for pods. Linkerd needs this functionality to deploy the
linkerd control plane itself, but also to run the proxy containers in any deployment that is going to be included in
the service mesh. Enabling `emptyDir` volumes poses a risk that a pod will create
such big `emptyDir` that the underlying cluster node will run out of disk space.
If you're OK with this potential issue, the easiest way to allow for `emptyDir`
for all the deployments is to edit the default PSP of your cluster by running the
command:

```bash
kubectl edit psp restricted
```

then finding the `spec.volumes` list and appending `emptyDir` value to the list. Then, write the file and exit your editor.

To finally deploy linkerd, run

```bash
kubectl apply -f linkerd-manifest.yaml
```

When installing via the Giant Swarm web UI, you'll need to apply the labels
and annotations listed in the `namespaceConfig` section above manually.

### Step 4: After deployment

- Disable proxy injections for pods running in the `kube-system` namespace by applying certain labels and annotations

```bash
kubectl annotate namespace kube-system linkerd.io/inject=disabled
kubectl label namespace kube-system config.linkerd.io/admission-webhooks=disabled
```

- Optional but recommended: You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.10.2).

- We strongly recommend installing the `linkerd viz` extension using the [`linkerd`](#usage-with-linkerd-cli) command.

Unfortunately, the template this generates uses some user IDs that are by default
not permitted by the default cluster's PSP. To allow for that in the default PSP,
edit it and change the value of `spec.runAsUser.ranges[0].min` to `472`.

```bash
linkerd viz install | kubectl apply -f -
```

After installation, you can open the dashboard by executing

```bash
linkerd viz dashboard
```

## Mesh your workloads

After installation, linkerd looks for a `linkerd.io/inject: enabled` annotation on `Namespaces` or other workload resources. Adding this annotation to your workload namespaces will trigger automatic proxy container injection to your pods. You can use the [`spec.namespaceConfig.annotations`](https://docs.giantswarm.io/app-platform/namespace-configuration/) field of your other apps `App` CR to automatically apply the required annotation.

More information on proxy injection can be found on the ["Automatic Proxy Injection" page](https://linkerd.io/2.10/features/proxy-injection/) in the upstream documentation.

**Attention**: Proxy containers are using `EmptyDir` volumes for storing ephemeral data, so all of your workload pods meshed by linkerd require a `PodSecurityPolicy` which allows use of `EmptyDir` volumes.

## Installing without the CNI plugin

In order to install this app without the CNI plugin, you'll need to specify `cniEnabled: false` in your user configuration.

Be aware that running without the CNI plugin, proxy containers will run as `root` and will require `NET_ADMIN` and `NET_RAW` capabilities.

## Troubleshooting

### App installation fails when I specify a namespace name other than `linkerd`

The `linkerd` namespace name is assumed in several parts of the chart, so we restricted installation to namespaces named `linkerd` only.

### Proxy containers fail to start

Your workload must be able to create `EmptyDir` volumes, so you'll need to create a `PodSecurityPolicy` allowing the creation of `EmptyDir` volumes.

Although not recommended, it is possible to edit the default `PodSecurityPolicy` named `restricted` to allow usage of`EmptyDir` volumes for all workloads without an own `PodSecurityPolicy`.

## Usage with `linkerd` cli

You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.10.2).

## Credit

- <https://linkerd.io/2.10/tasks/install-helm/>

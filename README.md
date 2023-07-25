# linkerd-control-plane chart

[![CircleCI](https://circleci.com/gh/giantswarm/linkerd-control-plane-app.svg?style=shield)](https://circleci.com/gh/giantswarm/linkerd-control-plane-app)

Linkerd2 service mesh for Giant Swarm clusters. Based on the official linkerd2 helm charts with a few changes, required to deploy to Giant Swarm clusters.

**Before you install this app, please review this document from start to finish!**

## Quickstart Guide

### Step 1: Pre-installation and Configuration

- Install the linkerd CNI plugin by installing [`linkerd2-cni-app`](https://github.com/giantswarm/linkerd2-cni-app) on your cluster. Be sure to review the instructions for the CNI plugin.
- A successful install will require you to generate a trust anchor and issuer certificate. The following steps loosely follow [the official instructions](https://linkerd.io/2.12/tasks/generate-certificates/).

Obtain the `step` cli (we're using `step_linux_0.19.0_amd64.tar.gz` from [here](https://github.com/smallstep/cli/releases/tag/v0.19.0)) and execute the following commands. Take note of the `--not-after` flag. (8760h = 1 year)

```bash
step certificate create root.linkerd.cluster.local ca.crt ca.key --profile root-ca --no-password --insecure --not-after=8760h
step certificate create identity.linkerd.cluster.local issuer.crt issuer.key --profile intermediate-ca --not-after=8760h --no-password --insecure --ca ca.crt --ca-key ca.key
```

- Finally construct your user secrets file by filling this template and saving as `my-linkerd-certificates.yaml`:

```yaml
identity:
  issuer:
    tls:
      crtPEM: |
        <contents of the issuer.crt file>
      keyPEM: |
        <contents of the issuer.key file>
identityTrustAnchorsPEM: |
  <contents of the ca.crt file>
```

- (Optional) Create a file `my-linkerd-values.yaml` with your [user configuration](https://docs.giantswarm.io/app-platform/app-configuration/). The user configuration should only contain values that are additional to or diverge from the default values provided by the chart. Check the link above to see how configurations are merged.
With the default values, Linkerd is installed in High-Availability mode and with CNI plugin enabled. Check the full list in the [README](https://github.com/giantswarm/linkerd-control-plane-app/blob/main/helm/linkerd-control-plane/README.md).

### Step 2: Deploy Linkerd

We recommend deploying the app by applying an `App` CR (Custom Resource) onto your management cluster. Use the [`kubectl gs`](https://docs.giantswarm.io/ui-api/kubectl-gs/) plugin to generate a valid `App` CR with command:

```bash
kubectl gs template app \
  --catalog giantswarm \
  --name linkerd-control-plane \
  --target-namespace linkerd \
  --cluster-name <your-cluster-id>  \
  --version 0.8.0 \
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
  name: linkerd-control-plane
  namespace: <your-cluster-id>
spec:
  catalog: giantswarm
  kubeConfig:
    inCluster: false
  name: linkerd-control-plane
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
      name: linkerd-control-plane-userconfig-<your-cluster-id>
      namespace: <your-cluster-id>
    secret:
      name: linkerd-control-plane-userconfig-<your-cluster-id>
      namespace: <your-cluster-id>
  version: 0.8.0
```

Please note, that for security reasons Giant Swarm by default forbids the usage of
`emptyDir` volumes as storage for pods. Linkerd needs this functionality to run the proxy containers in any deployment that is going to be included in
the service mesh. Enabling `emptyDir` volumes poses a risk that a pod will create
such big `emptyDir` that the underlying cluster node will run out of disk space.
If you're OK with this potential issue, the easiest way to allow for `emptyDir`
for all the deployments is to edit the default PSP of your cluster by running the
command:

```bash
kubectl patch psp restricted --type='json' -p='[{"op": "add", "path": "/spec/volumes/-", "value": "emptyDir"}]'
```

Now you're ready to deploy linkerd - run the following command:

```bash
kubectl apply -f linkerd-manifest.yaml
```

When installing via the Giant Swarm web UI, you'll need to apply the labels
and annotations listed in the `namespaceConfig` section above manually.

### Step 3: After deployment

- Optional but recommended: You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.12.4).

- Optionally you can also install the `linkerd-viz` extension using the [`linkerd-viz App`](https://github.com/giantswarm/linkerd-viz-app/).

After installation, you can open the dashboard by executing

```bash
linkerd viz dashboard
```

## Mesh your workloads

After installation, linkerd looks for a `linkerd.io/inject: enabled` annotation on `Namespaces` or other workload resources. Adding this annotation to your workload namespaces will trigger automatic proxy container injection to your pods. You can use the [`spec.namespaceConfig.annotations`](https://docs.giantswarm.io/app-platform/namespace-configuration/) field of your other apps `App` CR to automatically apply the required annotation.

More information on proxy injection can be found on the ["Automatic Proxy Injection" page](https://linkerd.io/2.12/features/proxy-injection/) in the upstream documentation.

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

### Failed Scheduling

The app is set up for 'High Availability' by default, with 3 replicas and pod anti-affinity enabled. However, on small clusters (with less than 3 worker nodes), this can cause scheduling failures when rolling pods or nodes. To prevent this, temporarily reduce .Values.controllerReplicas to 2.

## Usage with `linkerd` cli

You can use the `linkerd` cli as usual with this app as we're using the default namespaces. (`linkerd` and `linkerd-cni`). You can download it from the [linkerd release page](https://github.com/linkerd/linkerd2/releases/tag/stable-2.12.1).

## Maintainer info

This chart is maintained using the vendir method. You need [vendir](https://github.com/vmware-tanzu/carvel-vendir) and [yq](https://github.com/mikefarah/yq) binaries for it to work.

Run `make upgrade-chart` to pull the last stable version of the chart from 
<https://github.com/giantswarm/linkerd2-upstream>.

## Credit

- <https://linkerd.io/2.12/tasks/install-helm/>

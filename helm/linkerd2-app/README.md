# linkerd2-app

Linkerd gives you observability, reliability, and security
for your microservices — with no code change required.

![Version: 0.8.0](https://img.shields.io/badge/Version-0.8.0-informational?style=flat-square)

![AppVersion: stable-2.11.4](https://img.shields.io/badge/AppVersion-stable--2.11.4-informational?style=flat-square)

**Homepage:** <https://github.com/giantswarm/linkerd2-app>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| linkerd-control-plane.clusterDomain | string | `"cluster.local"` | Kubernetes DNS Domain name to use |
| linkerd-control-plane.clusterNetworks | string | `"10.0.0.0/8,100.64.0.0/10,172.16.0.0/12,192.168.0.0/16"` | The cluster networks for which service discovery is performed. This should include the pod and service networks, but need not include the node network.  By default, all private networks are specified so that resolution works in typical Kubernetes environments. |
| linkerd-control-plane.cniEnabled | bool | `true` | enabling this omits the NET_ADMIN capability in the PSP and the proxy-init container when injecting the proxy; requires the linkerd-cni plugin to already be installed |
| linkerd-control-plane.controlPlaneTracing | bool | `false` | enables control plane tracing |
| linkerd-control-plane.controlPlaneTracingNamespace | string | `"linkerd-jaeger"` | namespace to send control plane traces to |
| linkerd-control-plane.controllerImage | string | `"giantswarm/linkerd2-controller"` |  |
| linkerd-control-plane.controllerLogFormat | string | `"plain"` | Log format for the control plane components |
| linkerd-control-plane.controllerLogLevel | string | `"info"` | Log level for the control plane components |
| linkerd-control-plane.controllerReplicas | int | `3` | Number of replicas for each control plane pod |
| linkerd-control-plane.controllerResources.cpu.limit | string | `""` |  |
| linkerd-control-plane.controllerResources.cpu.request | string | `"100m"` |  |
| linkerd-control-plane.controllerResources.memory.limit | string | `"250Mi"` |  |
| linkerd-control-plane.controllerResources.memory.request | string | `"50Mi"` |  |
| linkerd-control-plane.controllerUID | int | `2103` | User ID for the control plane components |
| linkerd-control-plane.debugContainer.image.name | string | `"giantswarm/linkerd2-debug"` | Docker image for the debug container |
| linkerd-control-plane.debugContainer.image.pullPolicy | string | imagePullPolicy | Pull policy for the debug container Docker image |
| linkerd-control-plane.debugContainer.image.version | string | linkerdVersion | Tag for the debug container Docker image |
| linkerd-control-plane.destinationResources.cpu.limit | string | `""` |  |
| linkerd-control-plane.destinationResources.cpu.request | string | `"100m"` |  |
| linkerd-control-plane.destinationResources.memory.limit | string | `"250Mi"` |  |
| linkerd-control-plane.destinationResources.memory.request | string | `"50Mi"` |  |
| linkerd-control-plane.disableHeartBeat | bool | `false` |  |
| linkerd-control-plane.enableEndpointSlices | bool | `false` | enables the use of EndpointSlice informers for the destination service; enableEndpointSlices should be set to true only if EndpointSlice K8s feature gate is on; the feature is still experimental. |
| linkerd-control-plane.enableH2Upgrade | bool | `true` | Allow proxies to perform transparent HTTP/2 upgrading |
| linkerd-control-plane.enablePSP | bool | `true` | Add a PSP resource and bind it to the control plane ServiceAccounts. Note PSP has been deprecated since k8s v1.21 |
| linkerd-control-plane.enablePodAntiAffinity | bool | `true` |  |
| linkerd-control-plane.enablePprof | bool | `false` | enables the use of pprof endpoints on control plane component's admin servers |
| linkerd-control-plane.identity.externalCA | bool | `false` | If the linkerd-identity-trust-roots ConfigMap has already been created |
| linkerd-control-plane.identity.issuer.clockSkewAllowance | string | `"20s"` | Amount of time to allow for clock skew within a Linkerd cluster |
| linkerd-control-plane.identity.issuer.issuanceLifetime | string | `"24h0m0s"` | Amount of time for which the Identity issuer should certify identity |
| linkerd-control-plane.identity.issuer.scheme | string | `"linkerd.io/tls"` |  |
| linkerd-control-plane.identity.issuer.tls | object | `{"crtPEM":"","keyPEM":""}` | Which scheme is used for the identity issuer secret format |
| linkerd-control-plane.identity.issuer.tls.crtPEM | string | `""` | Issuer certificate (ECDSA). It must be provided during install. |
| linkerd-control-plane.identity.issuer.tls.keyPEM | string | `""` | Key for the issuer certificate (ECDSA). It must be provided during install |
| linkerd-control-plane.identityResources.cpu.limit | string | `""` |  |
| linkerd-control-plane.identityResources.cpu.request | string | `"100m"` |  |
| linkerd-control-plane.identityResources.memory.limit | string | `"250Mi"` |  |
| linkerd-control-plane.identityResources.memory.request | string | `"10Mi"` |  |
| linkerd-control-plane.identityTrustAnchorsPEM | string | `""` | Trust root certificate (ECDSA). It must be provided during install. |
| linkerd-control-plane.identityTrustDomain | string | clusterDomain | Trust domain used for identity |
| linkerd-control-plane.image | object | `{"registry":"quay.io"}` | Registry switch Do not overwrite this as it is automatically set based on the installation region |
| linkerd-control-plane.imagePullPolicy | string | `"IfNotPresent"` | Docker image pull policy |
| linkerd-control-plane.imagePullSecrets | list | `[]` | For Private docker registries, authentication is needed.  Registry secrets are applied to the respective service accounts |
| linkerd-control-plane.installNamespace | bool | `false` |  |
| linkerd-control-plane.linkerdVersion | string | `"stable-2.11.4"` | control plane version. See Proxy section for proxy version |
| linkerd-control-plane.namespace | string | `"linkerd"` | Control plane namespace |
| linkerd-control-plane.nodeSelector | object | `{"kubernetes.io/os":"linux"}` | NodeSelector section, See the [K8S documentation](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/#nodeselector) for more information |
| linkerd-control-plane.podAnnotations | object | `{}` | Additional annotations to add to all pods |
| linkerd-control-plane.podLabels | object | `{}` | Additional labels to add to all pods |
| linkerd-control-plane.policyController.defaultAllowPolicy | string | "all-unauthenticated" | The default allow policy to use when no `Server` selects a pod.  One of: "all-authenticated", "all-unauthenticated", "cluster-authenticated", "cluster-unauthenticated", "deny" |
| linkerd-control-plane.policyController.image.name | string | `"giantswarm/linkerd2-policy-controller"` | Docker image for the proxy |
| linkerd-control-plane.policyController.image.pullPolicy | string | imagePullPolicy | Pull policy for the proxy container Docker image |
| linkerd-control-plane.policyController.image.version | string | linkerdVersion | Tag for the proxy container Docker image |
| linkerd-control-plane.policyController.logLevel | string | `"linkerd=info,warn"` | Log level for the policy controller |
| linkerd-control-plane.policyController.resources | object | destinationResources | policy controller resource requests & limits |
| linkerd-control-plane.policyController.resources.cpu.limit | string | `""` | Maximum amount of CPU units that the policy controller can use |
| linkerd-control-plane.policyController.resources.cpu.request | string | `""` | Amount of CPU units that the policy controller requests |
| linkerd-control-plane.policyController.resources.memory.limit | string | `""` | Maximum amount of memory that the policy controller can use |
| linkerd-control-plane.policyController.resources.memory.request | string | `""` | Maximum amount of memory that the policy controller requests |
| linkerd-control-plane.policyValidator.caBundle | string | `""` | Bundle of CA certificates for policy validator. If not provided then Helm will use the certificate generated  for `policyValidator.crtPEM`. If `policyValidator.externalSecret` is set to true, this value must be set, as no certificate will be generated. |
| linkerd-control-plane.policyValidator.crtPEM | string | `""` | Certificate for the policy validator. If not provided then Helm will generate one. |
| linkerd-control-plane.policyValidator.externalSecret | bool | `false` | Do not create a secret resource for the policyValidator webhook. If this is set to `true`, the value `policyValidator.caBundle` must be set (see below). |
| linkerd-control-plane.policyValidator.keyPEM | string | `""` | Certificate key for the policy validator. If not provided then Helm will generate one. |
| linkerd-control-plane.policyValidator.namespaceSelector | object | `{"matchExpressions":[{"key":"config.linkerd.io/admission-webhooks","operator":"NotIn","values":["disabled"]}]}` | Namespace selector used by admission webhook |
| linkerd-control-plane.postHookInitHack | object | `{"enabled":true,"image":"giantswarm/alpine:3.15.5"}` | postHookInitHack There is a race condition in Kubernetes for cluster running a CNI different than calico as primary together with Calico as a policy engine (network policies). This is a workaround to make it work it. More info in https://github.com/giantswarm/roadmap/issues/1174 |
| linkerd-control-plane.profileValidator.caBundle | string | `""` | Bundle of CA certificates for service profile validator. If not provided then Helm will use the certificate generated  for `profileValidator.crtPEM`. If `profileValidator.externalSecret` is set to true, this value must be set, as no certificate will be generated. |
| linkerd-control-plane.profileValidator.crtPEM | string | `""` | Certificate for the service profile validator. If not provided then Helm will generate one. |
| linkerd-control-plane.profileValidator.externalSecret | bool | `false` | Do not create a secret resource for the profileValidator webhook. If this is set to `true`, the value `profileValidator.caBundle` must be set (see below). |
| linkerd-control-plane.profileValidator.keyPEM | string | `""` | Certificate key for the service profile validator. If not provided then Helm will generate one. |
| linkerd-control-plane.profileValidator.namespaceSelector | object | `{"matchExpressions":[{"key":"config.linkerd.io/admission-webhooks","operator":"NotIn","values":["disabled"]}]}` | Namespace selector used by admission webhook |
| linkerd-control-plane.proxy.await | bool | `true` |  |
| linkerd-control-plane.proxy.cores | int | `0` | The `cpu.limit` and `cores` should be kept in sync. The value of `cores` must be an integer and should typically be set by rounding up from the limit. E.g. if cpu.limit is '1500m', cores should be 2. |
| linkerd-control-plane.proxy.enableExternalProfiles | bool | `false` | Enable service profiles for non-Kubernetes services |
| linkerd-control-plane.proxy.image.name | string | `"giantswarm/linkerd2-proxy"` | Docker image for the proxy |
| linkerd-control-plane.proxy.image.pullPolicy | string | imagePullPolicy | Pull policy for the proxy container Docker image |
| linkerd-control-plane.proxy.image.version | string | linkerdVersion | Tag for the proxy container Docker image |
| linkerd-control-plane.proxy.inboundConnectTimeout | string | `"100ms"` | Maximum time allowed for the proxy to establish an inbound TCP connection |
| linkerd-control-plane.proxy.logFormat | string | `"plain"` | Log format (`plain` or `json`) for the proxy |
| linkerd-control-plane.proxy.logLevel | string | `"warn,linkerd=info"` | Log level for the proxy |
| linkerd-control-plane.proxy.opaquePorts | string | `"25,587,3306,4444,5432,6379,9300,11211"` | Default set of opaque ports - SMTP (25,587) server-first - MYSQL (3306) server-first - Galera (4444) server-first - PostgreSQL (5432) server-first - Redis (6379) server-first - ElasticSearch (9300) server-first - Memcached (11211) clients do not issue any preamble, which breaks detection |
| linkerd-control-plane.proxy.outboundConnectTimeout | string | `"1000ms"` | Maximum time allowed for the proxy to establish an outbound TCP connection |
| linkerd-control-plane.proxy.ports.admin | int | `4191` | Admin port for the proxy container |
| linkerd-control-plane.proxy.ports.control | int | `4190` | Control port for the proxy container |
| linkerd-control-plane.proxy.ports.inbound | int | `4143` | Inbound port for the proxy container |
| linkerd-control-plane.proxy.ports.outbound | int | `4140` | Outbound port for the proxy container |
| linkerd-control-plane.proxy.requireIdentityOnInboundPorts | string | `""` |  |
| linkerd-control-plane.proxy.resources.cpu.limit | string | `""` | Maximum amount of CPU units that the proxy can use |
| linkerd-control-plane.proxy.resources.cpu.request | string | `"100m"` | Amount of CPU units that the proxy requests |
| linkerd-control-plane.proxy.resources.memory.limit | string | `"250Mi"` | Maximum amount of memory that the proxy can use |
| linkerd-control-plane.proxy.resources.memory.request | string | `"20Mi"` | Maximum amount of memory that the proxy requests |
| linkerd-control-plane.proxy.uid | int | `2102` | User id under which the proxy runs |
| linkerd-control-plane.proxy.waitBeforeExitSeconds | int | `0` | If set the proxy sidecar will stay alive for at least the given period before receiving SIGTERM signal from Kubernetes but no longer than pod's `terminationGracePeriodSeconds`. See [Lifecycle hooks](https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks) for more info on container lifecycle hooks. |
| linkerd-control-plane.proxyInit.closeWaitTimeoutSecs | int | `0` |  |
| linkerd-control-plane.proxyInit.ignoreInboundPorts | string | `"4190,4191,4567,4568"` | Default set of inbound ports to skip via iptables - linkerd (4190,4191) - Galera (4567,4568) |
| linkerd-control-plane.proxyInit.ignoreOutboundPorts | string | `"4190,4191,4567,4568"` | Default set of outbound ports to skip via iptables - linkerd (4190,4191) - Galera (4567,4568) |
| linkerd-control-plane.proxyInit.image.name | string | `"giantswarm/linkerd2-proxy-init"` | Docker image for the proxy-init container |
| linkerd-control-plane.proxyInit.image.pullPolicy | string | imagePullPolicy | Pull policy for the proxy-init container Docker image |
| linkerd-control-plane.proxyInit.image.version | string | `"v1.5.3"` | Tag for the proxy-init container Docker image |
| linkerd-control-plane.proxyInit.logFormat | string | plain | Log format (`plain` or `json`) for the proxy-init |
| linkerd-control-plane.proxyInit.logLevel | string | info | Log level for the proxy-init |
| linkerd-control-plane.proxyInit.resources.cpu.limit | string | `"100m"` | Maximum amount of CPU units that the proxy-init container can use |
| linkerd-control-plane.proxyInit.resources.cpu.request | string | `"10m"` | Amount of CPU units that the proxy-init container requests |
| linkerd-control-plane.proxyInit.resources.memory.limit | string | `"50Mi"` | Maximum amount of memory that the proxy-init container can use |
| linkerd-control-plane.proxyInit.resources.memory.request | string | `"10Mi"` | Amount of memory that the proxy-init container requests |
| linkerd-control-plane.proxyInit.runAsRoot | bool | `true` | Allow overriding the runAsNonRoot behaviour |
| linkerd-control-plane.proxyInit.skipSubnets | string | `""` | Comma-separated list of subnets in valid CIDR format that should be skipped by the proxy |
| linkerd-control-plane.proxyInit.xtMountPath.mountPath | string | `"/run"` |  |
| linkerd-control-plane.proxyInit.xtMountPath.name | string | `"linkerd-proxy-init-xtables-lock"` |  |
| linkerd-control-plane.proxyInjector.caBundle | string | `""` | Bundle of CA certificates for proxy injector. If not provided then Helm will use the certificate generated  for `proxyInjector.crtPEM`. If `proxyInjector.externalSecret` is set to true, this value must be set, as no certificate will be generated. |
| linkerd-control-plane.proxyInjector.crtPEM | string | `""` | Certificate for the proxy injector. If not provided then Helm will generate one. |
| linkerd-control-plane.proxyInjector.externalSecret | bool | `false` | Do not create a secret resource for the profileValidator webhook. If this is set to `true`, the value `proxyInjector.caBundle` must be set (see below) |
| linkerd-control-plane.proxyInjector.keyPEM | string | `""` | Certificate key for the proxy injector. If not provided then Helm will generate one. |
| linkerd-control-plane.proxyInjector.namespaceSelector | object | `{"matchExpressions":[{"key":"config.linkerd.io/admission-webhooks","operator":"NotIn","values":["disabled"]}]}` | Namespace selector used by admission webhook. If not set defaults to all namespaces without the annotation config.linkerd.io/admission-webhooks=disabled |
| linkerd-control-plane.proxyInjectorResources.cpu.limit | string | `""` |  |
| linkerd-control-plane.proxyInjectorResources.cpu.request | string | `"100m"` |  |
| linkerd-control-plane.proxyInjectorResources.memory.limit | string | `"250Mi"` |  |
| linkerd-control-plane.proxyInjectorResources.memory.request | string | `"50Mi"` |  |
| linkerd-control-plane.webhookFailurePolicy | string | `"Fail"` | Failure policy for the proxy injector |

----------------------------------------------
Autogenerated from chart metadata using [helm-docs v1.11.0](https://github.com/norwoodj/helm-docs/releases/v1.11.0)

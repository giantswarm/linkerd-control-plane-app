# Using Vault as Linkerd's trust anchor

## Overview

cert-manager will authenticate to Vault by using a dedicated Kubernetes ServiceAccount which is created specifically for this purpose. This must exist in the `linkerd` namespace _before_ the Chart is installed. The ServiceAccount's details will then be used to configure the `kubernetes` authentication method for Vault. Both of these steps must be carried out before the Chart can be installed in order to permit creation of the necessary TLS certificates required for Linkerd to function.
## Pre-requisites

**cert-manager**

- cert-manager must already be running in the cluster.

**Vault**

Vault must already be running in a location which is accessible to the cluster. If Vault will be used to provide a shared trust anchoer for two clusters running in `multicluster` mode then it must be accessible from both clusters.

Requirements:

- A PKI endpoint configured to allow CA cert creation with the following minimum role requirements:
  - `allow_bare_domains=true allowed_domains="identity.linkerd.cluster.local"`
- A Kubernetes auth endpoint configured with the credentials of the dedicated ServiceAccount created below.
- A policy bound to the ServiceAccount which allows it to perform the following operations on the PKI endpoint:
```
path "pki*"               { capabilities = ["read", "list"] }
path "pki/roles/rolename" { capabilities = ["create", "update"] }
path "pki/sign/rolename"  { capabilities = ["create", "update"] }
path "pki/issue/rolename" { capabilities = ["create"] }
```

## Cluster configuration

- first declare some variables:
```
export SA_NAME=linkerd-vault-auth
export LINKERD_NAMESPACE=linkerd # this must match the namespace the Chart is installed in later.
```
- create the namespace:
```
kubectl create namespace ${LINKERD_NAMESPACE}
```
- create the ServiceAccount:
```
kubectl create -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ${SA_NAME}
  namespace: ${LINKERD_NAMESPACE}
EOF
```
- get the name of the ServiceAccount's associated secret:
```
SA_SECRET_NAME=$(kubectl get sa ${SA_NAME} -n ${LINKERD_NAMESPACE} \
  -o jsonpath="{.secrets[*]['name']}")
```
- get the ServiceAccount's JWT token:
```
SA_TOKEN=$(kubectl get secret ${SA_SECRET_NAME} -n ${LINKERD_NAMESPACE} \
  -o jsonpath={'.data.token'} | base64 -d)
```
- get the cluster's CA certificate:
```
kubectl get secret ${SA_SECRET_NAME} -n ${LINKERD_NAMESPACE} \
  | base64 -d > /tmp/k8s-ca.crt
```


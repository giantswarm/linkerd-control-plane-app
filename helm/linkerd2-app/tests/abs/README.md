# linkerd2-app tests

We want to ensure this app can be installed without any issues, so we're executing these tests.

## General test flow

- Add giantswarm catalog
- Add giantswarm-test catalog
- Install [linkerd2-cni-app](https://github.com/giantswarm/linkerd2-cni-app) from giantswarm-test catalog
- Install this chart
- Install a test app ?
- Execute `linkerd check --cni-namespace linkerd2-cni-app --linkerd-namespace linkerd2-app --output json --proxy --namespace test-app-namespace`


## Updating the test certificates

TODO

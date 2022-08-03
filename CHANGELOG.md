# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.7.1] - 2022-08-03

### Changed

- Update pytest-helm-charts from beta to v0.7.0 ([#84](https://github.com/giantswarm/linkerd2-app/pull/84))
- Add an init container to destination and injector services to avoid the [known issue](https://github.com/projectcalico/calico/issues/3499) of missing IP in post hook action

## [0.7.0] - 2022-05-13

Please be aware that linkerd will never recreate existing pods to update the injected proxy container image version. This will happen the next time your meshed pods will restart.

### Changed

- Align with and upgrade to upstream `stable-2.11.2`. ([#79](https://github.com/giantswarm/linkerd2-app/pull/79))

## [0.6.2] - 2021-11-03

### Changed

- Update app metadata

## [0.6.1] - 2021-08-27

### Changed

- Specifically ignore the control and admin ports when intialising the proxies ([#48](https://github.com/giantswarm/linkerd2-app/pull/48))

## [0.6.0] - 2021-08-03

### Changed

- Align with and upgrade to upstream `stable-2.10.2`. ([#41](https://github.com/giantswarm/linkerd2-app/pull/41))
- First release published to the `giantswarm` catalog.

## [0.5.1] - 2020-12-18

### Changed

- Make namespace-tagger hook more resilient. ([#29](https://github.com/giantswarm/linkerd2-app/pull/29))

## [0.5.0] - 2020-12-17

### Changed

- Update chart to `stable-2.9.1`. ([#26](https://github.com/giantswarm/linkerd2-app/pull/26))

## [0.4.2] - 2020-12-16

### Changed

- Disable Prometheus integration by default. ([#22](https://github.com/giantswarm/linkerd2-app/pull/22))

### Added

- Added a values.schema.json file to help with validating user values.

## [0.4.1] - 2020-10-13

### Fixed

- Allowed tracing subchart's serviceaccounts to use the PSP. ([#7](https://github.com/giantswarm/linkerd2-app/pull/7))
- Corrected YAML anchor usage in values.yaml. ([#9](https://github.com/giantswarm/linkerd2-app/pull/9))

## [0.4.0] - 2020-10-09

### Changed

- Updated to upstream v2.8.1. ([#4](https://github.com/giantswarm/linkerd2-app/pull/4))
- Made namespace configurable to align with Giant Swarm best practises. ([#4](https://github.com/giantswarm/linkerd2-app/pull/4))

## [0.3.2] 2020-05-05

### Changed

- Update chart to v2.7.1.

[Unreleased]: https://github.com/giantswarm/linkerd2-app/compare/v0.7.1...HEAD
[0.7.1]: https://github.com/giantswarm/linkerd2-app/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/giantswarm/linkerd2-app/compare/v0.6.2...v0.7.0
[0.6.2]: https://github.com/giantswarm/linkerd2-app/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/giantswarm/linkerd2-app/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/giantswarm/linkerd2-app/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/giantswarm/linkerd2-app/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/giantswarm/linkerd2-app/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/giantswarm/linkerd2-app/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/giantswarm/linkerd2-app/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/giantswarm/linkerd2-app/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/giantswarm/linkerd2-app/releases/tag/v0.3.2

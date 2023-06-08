# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Replace icon and add logo.
- Upgrade to Linkerd v2.13.3.

## [0.11.0] - 2023-03-09

### Changed

- Upgrade to linkerd v2.12.4

## [0.10.0] - 2023-03-07

### Changed

- Changes linkerd priority class to "giantswarm-critical" to improve scheduling.

## [0.9.0] - 2023-01-31

### Changed

- Sync with upstream repo [#120](https://github.com/giantswarm/linkerd-control-plane-app/pull/120).
  - Add templated values for noop image 
  - Move giantswarm labels into partials chart
  - Fix workflow for automated PR creation
- Avoids the proxy-injector to inspect giantswarm namespace. To mitigate issues we saw with the chart-operator running there.

## [0.8.0] - 2022-10-27

### Changed

- Rename app as `linkerd-control-plane` ([#117](https://github.com/giantswarm/linkerd-control-plane-app/pull/117)).
- Bump version 2.12.2 ([#116](https://github.com/giantswarm/linkerd-control-plane-app/pull/116)).

## [0.7.5] - 2022-10-13

### Changed

- Add image registry switch to automatically switch the used image registry based on the installation region

### Removed

- Post hook init hack when CNI is disabled since there's another init container around already.

## [0.7.4] - 2022-08-25

### Changed

- Align with upstream release `stable-2.11.4`
- Fix security for when a user manually specified the `policyValidator.keyPEM` setting
- Multiple smaller fixes around `linkerd-multicluster`
- For details see upstream [changelog entry for version stable-2.11.4](https://github.com/linkerd/linkerd2/blob/stable-2.11.4/CHANGES.md#stable-2114) and [stable-2.11.3](https://github.com/linkerd/linkerd2/blob/stable-2.11.4/CHANGES.md#stable-2113)

## [0.7.3] - 2022-08-10

### Changed

- Make image configurable in post start init procedure.
- Fix postHookInitHack check in deployments.

## [0.7.2] - 2022-08-03

### Changed

- Add Giant Swarm team label to resources.

## [0.7.1] - 2022-08-03

### Changed

- Update pytest-helm-charts from beta to v0.7.0 ([#84](https://github.com/giantswarm/linkerd-control-plane-app/pull/84))
- Add an init container to destination and injector services to avoid the [known issue](https://github.com/projectcalico/calico/issues/3499) of missing IP in post hook action

## [0.7.0] - 2022-05-13

Please be aware that linkerd will never recreate existing pods to update the injected proxy container image version. This will happen the next time your meshed pods will restart.

### Changed

- Align with and upgrade to upstream `stable-2.11.2`. ([#79](https://github.com/giantswarm/linkerd-control-plane-app/pull/79))

## [0.6.2] - 2021-11-03

### Changed

- Update app metadata

## [0.6.1] - 2021-08-27

### Changed

- Specifically ignore the control and admin ports when intialising the proxies ([#48](https://github.com/giantswarm/linkerd-control-plane-app/pull/48))

## [0.6.0] - 2021-08-03

### Changed

- Align with and upgrade to upstream `stable-2.10.2`. ([#41](https://github.com/giantswarm/linkerd-control-plane-app/pull/41))
- First release published to the `giantswarm` catalog.

## [0.5.1] - 2020-12-18

### Changed

- Make namespace-tagger hook more resilient. ([#29](https://github.com/giantswarm/linkerd-control-plane-app/pull/29))

## [0.5.0] - 2020-12-17

### Changed

- Update chart to `stable-2.9.1`. ([#26](https://github.com/giantswarm/linkerd-control-plane-app/pull/26))

## [0.4.2] - 2020-12-16

### Changed

- Disable Prometheus integration by default. ([#22](https://github.com/giantswarm/linkerd-control-plane-app/pull/22))

### Added

- Added a values.schema.json file to help with validating user values.

## [0.4.1] - 2020-10-13

### Fixed

- Allowed tracing subchart's serviceaccounts to use the PSP. ([#7](https://github.com/giantswarm/linkerd-control-plane-app/pull/7))
- Corrected YAML anchor usage in values.yaml. ([#9](https://github.com/giantswarm/linkerd-control-plane-app/pull/9))

## [0.4.0] - 2020-10-09

### Changed

- Updated to upstream v2.8.1. ([#4](https://github.com/giantswarm/linkerd-control-plane-app/pull/4))
- Made namespace configurable to align with Giant Swarm best practises. ([#4](https://github.com/giantswarm/linkerd-control-plane-app/pull/4))

## [0.3.2] 2020-05-05

### Changed

- Update chart to v2.7.1.

[Unreleased]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.11.0...HEAD
[0.11.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.7.5...v0.8.0
[0.7.5]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.7.4...v0.7.5
[0.7.4]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.7.3...v0.7.4
[0.7.3]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.7.2...v0.7.3
[0.7.2]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.7.1...v0.7.2
[0.7.1]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.7.0...v0.7.1
[0.7.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.6.2...v0.7.0
[0.6.2]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.5.1...v0.6.0
[0.5.1]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.5.0...v0.5.1
[0.5.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.4.2...v0.5.0
[0.4.2]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/giantswarm/linkerd-control-plane-app/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/giantswarm/linkerd-control-plane-app/releases/tag/v0.3.2

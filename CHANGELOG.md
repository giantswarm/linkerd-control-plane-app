# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project's packages adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/giantswarm/linkerd2-app/compare/v0.4.2...HEAD
[0.4.2]: https://github.com/giantswarm/linkerd2-app/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/giantswarm/linkerd2-app/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/giantswarm/linkerd2-app/compare/v0.3.2...v0.4.0
[0.3.2]: https://github.com/giantswarm/linkerd2-app/releases/tag/v0.3.2

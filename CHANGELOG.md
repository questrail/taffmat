# CHANGELOG.md

This file contains all notable changes to the [taffmat][] project.

## Unreleased

### Changed
- Updated dependencies in `requirements.txt`
- Removed `osx` from `.travis.yml`

### Fixed
- Wrong package was called in test task.

## v0.4.0 - 2015-08-20

### Added
- Invoke `inv test` task now provides coverage report.

### Changed
- Migrated from Travis legacy to container-based infrastructure
- Updated numpy to 1.9.2
- Updated other pip requirements

## v0.3.4 - 2014-08-19

### Bug Fixes
- `pip install taffmat` failed because `README.md` was missing. Fixed by
  replacing `README.rst` in the `MANIFSET.in` with `README.md`

## v0.3.3 - 2014-08-08

- Moved AUTHORS.txt to AUTHORS.md
- Moved CHANGES.md to CHANGELOG.md
- Switched to shields.io badges
- Updated README.md

## v0.3, 0.3.1, 0.3.2 - 2014-08-07

### Enhancements
- Made Python 3.3 & 3.4 compatible [isuee-8][]


## v0.2.9/0.2.10 - 2014-08-06

### Bug Fixes
- Update DATASET filed when writing .HDR file [issue-6][]


## v0.2.1-0.2.8 - 2014-08-06

### Bug Fixes
- PyPi automated deployment via Travis-CI


## v0.2 - 2014-08-06

### Enhancements
- Travis-CI testing and PyPi deployment ([issue-1][])
- Added function to change slope
- Write slices of `data_array` ([issue-3][])
- Add test for writing slice ([issue-4][])
- Changed to uppercase `.HDR` and `.DAT`
- Remove voice memo when saving slice ([issue-7][])

### Bug Fixes
- Use Windows carriage returns in `.HDR` file ([issue-5][])


## v0.1.2 - 2013-02-11

### Enhancements
- Changed to README.md
- Handle different data recorder models

### Bug Fixes
- Determine if .dat was saved as 2-byte or 4-byte data


## v0.1.1 - 2013-02-11

- Removed QuEST Rail LLC copyright.

## v0.1.0 - 2013-02-11

- Initial release has the ability to read/write LX-10 created TAFFmat
  files.

[issue-1]: https://github.com/questrail/taffmat/issues/1
[issue-3]: https://github.com/questrail/taffmat/issues/3
[issue-4]: https://github.com/questrail/taffmat/issues/4
[issue-5]: https://github.com/questrail/taffmat/issues/5
[issue-6]: https://github.com/questrail/taffmat/issues/6
[issue-7]: https://github.com/questrail/taffmat/issues/7
[issue-8]: https://github.com/questrail/taffmat/issues/8
[taffmat]: https://github.com/questrail/taffmat

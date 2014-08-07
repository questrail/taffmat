# Changelog

## develop (unreleased)

## 0.3/0.3.2 (August 7, 2014)

### Features

- Made Python 3.3 & 3.4 compatible [isuee-8][]

## 0.2.9/0.2.10 (August 6, 2014)

### Bug Fixes

- Update DATASET filed when writing .HDR file [issue-6][]

## 0.2.1-0.2.8 (August 6, 2014)

### Bug Fixes

- PyPi automated deployment via Travis-CI

## 0.2 (August 6, 2014)

### Features

- Travis-CI testing and PyPi deployment ([issue-1][])
- Added function to change slope
- Write slices of `data_array` ([issue-3][])
- Add test for writing slice ([issue-4][])
- Changed to uppercase `.HDR` and `.DAT`
- Remove voice memo when saving slice ([issue-7][])

### Bug Fixes

- Use Windows carriage returns in `.HDR` file ([issue-5][])

## 0.1.2 (February 11, 2013)

- Changed to README.md
- Determine if .dat was saved as 2-byte or 4-byte data
- Handle different data recorder models

## 0.1.1 (February 11, 2013)

- Removed QuEST Rail LLC copyright.

## 0.1.0 (February 11, 2013)

- Initial release has the ability to read/write LX-10 created TAFFmat
  files.

[issue-1]: https://github.com/questrail/taffmat/issues/1
[issue-3]: https://github.com/questrail/taffmat/issues/3
[issue-4]: https://github.com/questrail/taffmat/issues/4
[issue-5]: https://github.com/questrail/taffmat/issues/5
[issue-6]: https://github.com/questrail/taffmat/issues/6
[issue-7]: https://github.com/questrail/taffmat/issues/7
[issue-8]: https://github.com/questrail/taffmat/issues/8

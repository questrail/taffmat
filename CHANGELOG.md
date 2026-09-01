# CHANGELOG.md

This file contains all notable changes to the [taffmat][] project.

## Unreleased

### Removed

- `just deploy`, which published from a laptop with `uv publish` against
  whatever credentials were lying around. The release workflow replaces
  it.
- `AUTHORS.md`, along with the pointer to it in the copyright notice. The
  notice named "AUTHORS.txt", a file this project has never had under that
  name, and neither it nor `AUTHORS.md` travels in the wheel: `license-files`
  carries `LICENSE.txt` into `dist-info/licenses/` and nothing carries the
  other. The file listed one author, no maintainers, and no contributors,
  which the git history records more accurately.

### Added

- Releases publish from a tag rather than from a laptop. `just release`
  refuses a dirty tree, a branch other than `master`, a `master` behind
  its upstream, an empty Unreleased section, or an existing tag; then
  lints and tests; then shows the entries waiting to ship beside the
  version each kind of bump would produce, and asks which to cut. It
  bumps the version, closes out the CHANGELOG, commits, and tags.
  Pushing the tag is what publishes. `just release-check` runs the
  refusals on their own.
- The release workflow waits on the whole CI run before it uploads
  anything, confirms the tag sits on `master` and matches the version in
  `pyproject.toml`, and authenticates to PyPI with
  [trusted publishing][], so there is no API token to paste, store, or
  leak. It signs a [PEP 740][] attestation for each distribution against
  the same identity, and creates a GitHub release carrying the CHANGELOG
  section for that version as its notes.
- Continuous integration on GitHub Actions, which this project had none
  of. Every push and pull request lints, checks formatting, type checks,
  and runs the suite on 3.12 and 3.13, the versions the classifiers
  claim. A second job installs the oldest numpy `pyproject.toml` allows,
  so the floor is a tested promise rather than a hopeful one. A third
  audits the workflows with [zizmor][], since they are the part of the
  repository that can mint a PyPI credential. Coverage goes to Coveralls
  from the 3.13 leg.
- `scripts/smoke_test_wheel.py`, which installs the built wheel where
  `src/` cannot be reached and checks the version, `__version__`, every
  public function, and `py.typed`. Every other check runs against the
  source tree, so this is the only one that can catch a packaging
  mistake. `just build` runs it after building.
- `just cov`, which runs the suite under coverage and writes both a
  terminal summary and `htmlcov/`, and the `pytest-cov` it needs. A
  floor of 86%, what the suite covers today, means uncovered code has to
  arrive with either a test or a deliberate edit to that line.
- `py.typed`, so that the type hints already written reach anyone
  installing the package. Without the marker a type checker treats an
  installed package as untyped and ignores its annotations.

### Fixed

- `_read_taffmat_hdr()` and `_read_taffmat_dat()` caught the
  `FileNotFoundError` from opening a file, printed a message, and then
  carried on to use a variable the `try` block never got to assign,
  raising `UnboundLocalError` from the line below. `read_taffmat()`
  checks that both files exist and raises before either is called, so
  neither block could be reached through the public API; called
  directly, they now raise the `FileNotFoundError` that `open()` gives
  rather than printing and failing on the next line.

### Changed

- The ruff rule set gains `PT` and `RUF`, which applyaf and siganalysis
  already select, and the reason for selecting a set explicitly is
  written down where the set is. `RUF` found eight values unpacked from
  a return and never used, now named with a leading underscore. `PT`
  objects to every assertion in the suite, which is written against
  `unittest.TestCase`; that is turned off for the tests rather than
  answered, since converting the suite to plain pytest asserts is worth
  doing on its own and not as a side effect of picking a rule set.
- Type checking is done by [pyright][] rather than [ty][], which is still
  a 0.0.x release, matching applyaf and siganalysis. It runs inside
  `just lint` rather than as a separate `just check` that every caller
  had to remember. It found the unbound variables recorded above.
- The license is declared as an SPDX expression with `license-files`,
  which is what replaced the `License ::` classifier that used to carry
  it. It is also what puts `LICENSE.txt` into `dist-info/licenses/`.
- The version is written in `pyproject.toml` rather than in
  `src/taffmat/__init__.py`, and `taffmat.__version__` now reads it back
  from the installed distribution metadata. Its value is unchanged and
  every caller keeps working. The version had to move for `uv version` to
  be able to read or bump it, which is what the release recipe is built
  on; uv refuses a project whose version is dynamic.
- `.python-version` is tracked rather than ignored. It decides the
  interpreter a contributor's `uv sync` builds against, and the file was
  being read while being excluded from the repository.
- Replaced the [Invoke][] `tasks.py` with a [just][] `Justfile`, matching the
  recipes and groups used by the other questrail projects.
- Moved to [uv][] and a `pyproject.toml` built by hatchling, replacing
  `setup.py`, `requirements.txt`, `setup.cfg`, `MANIFEST`, and `MANIFEST.in`.
- Moved the module to a src layout at `src/taffmat/__init__.py`.
- Swapped the tooling: ruff for pep8/flake8, pytest for nose2, and ty for
  mypy. The code was reformatted by ruff and updated to f-strings.
- Raised the minimum Python to 3.12 and numpy to 2.2.

### Removed

- The `.travis.yml` config and the Travis CI and Coveralls README badges.
  Neither service runs for this project any more.

## v1.0.1 - 2017-11-16
- Bumped version

## v1.0.0 - 2017-11-16

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
[invoke]: https://www.pyinvoke.org/
[just]: https://just.systems
[PEP 740]: https://peps.python.org/pep-0740/
[pyright]: https://microsoft.github.io/pyright/
[taffmat]: https://github.com/questrail/taffmat
[ty]: https://github.com/astral-sh/ty
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
[zizmor]: https://docs.zizmor.sh/

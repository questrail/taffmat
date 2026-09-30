# CHANGELOG.md

This file contains all notable changes to the [taffmat][] project.

## Unreleased

### Added

- `__all__` names the public API: `read_taffmat`, `write_taffmat`,
  `write_taffmat_slice`, and `change_slope`. `from taffmat import *` no longer
  also pulls in the modules taffmat itself imports (`os`, `np`, `OrderedDict`,
  and `datetime`), and type checkers and editors now see those four names as
  the whole of the package's surface.

### Fixed

- `just add`, `just dev`, `just up`, and `just doc` quote the argument they
  are given. just interpolates an argument straight into the shell line, so
  `just add 'siganalysis>=0.10.0'` ran `uv add siganalysis>=0.10.0`: the `>`
  redirected stdout, uv saw the bare package name, the version constraint was
  dropped, and an empty file called `=0.10.0` was left in the repository root.
  Nothing failed, so the only sign it had happened was the stray file and a
  `pyproject.toml` that had not moved. The variadic `*args` that `test` and
  `cov` take stays unquoted, since quoting it would collapse several arguments
  into one.

## v3.0.1 - 2026-09-21

### Fixed

- `read_taffmat` puts sample n of the returned `time_vector` at
  `n / sampling_frequency_hz`. It spread the samples over
  `number_of_samples / sampling_frequency_hz` with `np.linspace`, which
  stretched every step by `N / (N - 1)` and placed each sample progressively
  late --- a full sample by the end of the recording. The error stayed under
  one sample throughout, so it moved no measurement, but it left the vector
  disagreeing with the times a caller works out from a sample index and the
  sampling frequency, which is how a caller that plots a waveform against
  `time_vector` and marks it up from sample indices ends up with the two
  slightly out of step.

## v3.0.0 - 2026-09-15

### Fixed

- `write_taffmat_slice` no longer modifies the `header_data` it is given. It
  aliased the caller's dictionary rather than copying it and then wrote the
  slice's description into it, so a caller that read a file, wrote a slice out
  of it, and went on using the header was silently handed the slice's numbers:
  `number_of_samples` became the length of the slice rather than of the
  recording, `voice_memo_on` became `False`, and `dataset` was renamed. The
  written .hdr file is unchanged; only the caller's copy is now left alone.
  The `dataset` assignment is dropped rather than moved onto the copy: the
  .hdr writer has always taken the `DATASET` line from the output filename it
  was handed, so setting the key did nothing but damage the caller's header.

### Added

- Ignore `.pypirc`. A copy holding a PyPI username and password predates the
  move to trusted publishing, which mints a short lived credential per
  release and leaves nothing on disk; nothing here needs the file, and
  ignoring it keeps a leftover from being committed by accident.

### Changed

- `just build` and `just release` depend on `cov` rather than `test`. CI runs
  pytest under coverage and fails below the `fail_under` floor in
  `pyproject.toml`, so the bare suite these recipes ran left that gate as one
  they never applied: a tree that passed locally could still be rejected on
  push, and `just release` could tag a version CI would then refuse to publish.
- Bring the `LICENSE.txt` copyright range up to 2026. It had stopped at
  2013, years behind the work in the file.

### Removed

- **Breaking:** `taffmat.__version__`. It was never read inside the package,
  only exported, and `importlib.metadata.version("taffmat")` has been the
  stdlib way to ask since 3.8, well below the 3.12 floor. Populating it
  cost roughly 7 ms at import time, for a name that duplicated what
  `pyproject.toml` already records. Read the version with
  `importlib.metadata.version("taffmat")`.

## v2.0.0 - 2026-09-01

### Added

- Python 3.14 to the classifiers and the CI matrix. The suite passes on
  it, and nothing in the dependencies held it back; it was left out only
  because the classifiers did not already name it.
- `just up-all` and a `Justfile` that is otherwise line for line the one
  in [applyaf][] and [siganalysis][], so that moving between the
  questrail projects does not mean learning a second set of recipe
  names.
- Dependabot keeps the pinned actions and the lock file moving. The
  actions in both workflows are pinned to commit SHAs, so a fix
  published upstream does not reach this repository the way it would
  behind a moving tag; without something to move them, pinning would
  amount to staying on one commit forever. It reads `pyproject.toml` and
  `uv.lock` together as well, so a dependency update arrives as a lock
  file change that CI checks with `uv sync --locked`.
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

- List `369937+matthewrankin@users.noreply.github.com` as the author
  address in `pyproject.toml`, replacing a work address. It is what
  `Author-email` carries in the built metadata and what PyPI shows on the
  project page, so it changes there from the next release onward.
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

- `just deploy`, which published from a laptop with `uv publish` against
  whatever credentials were lying around. The release workflow replaces
  it.
- `AUTHORS.md`, along with the pointer to it in the copyright notice. The
  notice named "AUTHORS.txt", a file this project has never had under that
  name, and neither it nor `AUTHORS.md` travels in the wheel: `license-files`
  carries `LICENSE.txt` into `dist-info/licenses/` and nothing carries the
  other. The file listed one author, no maintainers, and no contributors,
  which the git history records more accurately.

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
[applyaf]: https://github.com/questrail/applyaf
[invoke]: https://www.pyinvoke.org/
[just]: https://just.systems
[PEP 740]: https://peps.python.org/pep-0740/
[pyright]: https://microsoft.github.io/pyright/
[siganalysis]: https://github.com/questrail/siganalysis
[taffmat]: https://github.com/questrail/taffmat
[ty]: https://github.com/astral-sh/ty
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
[zizmor]: https://docs.zizmor.sh/

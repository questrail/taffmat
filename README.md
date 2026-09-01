# taffmat

[![PyPI Version][pypi ver image]][pypi ver link]
[![Python Versions][pyversions image]][pypi ver link]
[![CI Status][ci image]][ci link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

A Python 3.12+ module for reading and writing Teac TAFFmat files.

## About the TAFFmat file format

TAFFmat is Teac's proprietary file format used to store data from their
LX series and other data recorders.

According to the Teac "LX Series Recording Unit Instruction Manual":

>  TAFFmat (an acronym for Teac Data Acquisition File Format) is a
>  file format composed of the following:
>
>  * a data file containing A/D (analog to digital) converted data. The
>    file is binary format with the extension dat.
>  * a header file containing information such as recording
>    conditions. The file is in text format with the extension hdr.

TAFFmat is a trademark of Teac Corporation.

### Data Recorders Using TAFFmat

The following data recorders store their data in the TAFFmat file format:

* Teac [LX-10/20][]
* Teac [LX-110/120][]
* Teac [WX-7000 Series][]
* Teac [es8][]

## Installation

You can install [taffmat][] either via the Python Package Index (PyPI)
or from source.

To install using pip:

```bash
$ pip install taffmat
```

**Source:** https://github.com/questrail/taffmat

## Requirements

[taffmat][] requires the following Python packages:

* [numpy][]

## Public API

The following functions are provided:

- `change_slope(data_array, series, gain)`
- `read_taffmat(input_file)`
- `write_taffmat(data_array, header_data, output_base_filename)`
- `write_taffmat_slice(data_array, header_data, output_base_filename,
                       starting_data_index, ending_data_index`


## Contributing

Contributions are welcome! To contribute please:

1. Fork the repository
2. Create a feature branch
3. Add code and tests
4. Pass lint and tests
5. Submit a [pull request][]


## Development Setup

The project is managed with [uv][], and the development tasks are [just][]
recipes.

```bash
$ brew install uv just
```

`uv sync` creates the virtualenv and installs the dependencies, including
the development group, and `just` on its own lists the available recipes.

```bash
$ uv sync
$ just
```

The most common recipes are:

```bash
$ just test    # Run the tests using pytest
$ just lint    # Check lint, formatting, types, and workflows
$ just fix     # Lint and format the code using ruff, applying fixes
$ just cov     # Run the tests and report coverage
$ just add X   # Add X as a dependency
$ just out     # List the outdated dependencies
```

[ruff][] and [pyright][] are deliberately absent from that `brew install`
line. Both are dev dependencies pinned in `uv.lock` and reached through
`uv run`, so every recipe and every CI job uses the same version. A `brew
install ruff` would put a second, unpinned copy on the path for an editor
to find, and ruff releases change how code is formatted: the editor would
then reformat code that `ruff format --check` rejects on the next run.


### Releasing to PyPI

`just release` cuts the release. It first checks that a release is
possible at all, then lints, type checks, and tests, then shows the
entries waiting under Unreleased and the version each kind of bump would
produce, and asks which to cut. Once answered it bumps the version, closes
out the CHANGELOG, updates the lock file, commits, and tags. Pushing the
tag is what publishes.

```bash
$ just release
...
Which release? [1] 1

Tagged v1.0.2. Publish it with:

    git push --follow-tags
```

The tag push runs the [release workflow][], which waits on the whole [CI
workflow][ci link] before it does anything else: the 3.12 and 3.13 matrix
and the dependency floor job. It then checks that the tagged commit is on
`master`, since a tag is only a pointer and one placed anywhere else would
otherwise publish whatever it points at, rechecks the tag against the
version in `pyproject.toml`, and builds.

Every check to that point runs against the source tree, so the workflow
then installs the wheel it just built somewhere `src/` is not on the path
and exercises it there, which is the only step that can catch a packaging
mistake. It uploads once that passes. There is no PyPI API token
anywhere: the workflow authenticates with [trusted publishing][], which
mints a short lived credential from the GitHub OIDC identity of that run.
That same identity signs a [PEP 740][] attestation for each distribution,
which PyPI serves beside the file it attests.

Uploading is followed by a [GitHub release][releases] for the tag,
carrying the CHANGELOG section for that version as its notes and the built
distributions as its assets.

Pushing the tag is the point of no return, since PyPI never lets a version
number be reused. Everything `just release` does is local and amendable
until then, and it refuses to start against a dirty working tree, off
`master`, on a `master` behind its upstream, with a CHANGELOG whose
Unreleased section is empty, or when the tag it would create already
exists. `just release-check` runs those refusals on their own.

`just build` runs the same checks and produces the same distributions
without releasing anything, which is the way to inspect what CI would
upload.

This depends on one piece of configuration that lives outside the
repository. A [trusted publisher][trusted publishing] has to be registered
for `taffmat` on PyPI, pointing at the `questrail/taffmat` repository, the
`release.yml` workflow, and the `pypi` environment. It is a one time setup
per project.


## License

[taffmat][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[ci image]: https://github.com/questrail/taffmat/actions/workflows/ci.yml/badge.svg?branch=master
[ci link]: https://github.com/questrail/taffmat/actions/workflows/ci.yml
[coveralls image]: https://coveralls.io/repos/github/questrail/taffmat/badge.svg?branch=master
[coveralls link]: https://coveralls.io/github/questrail/taffmat?branch=master
[es8]: http://teac-ipd.com/data-recorders/es8/
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[just]: https://just.systems
[license image]: https://img.shields.io/pypi/l/taffmat.svg
[LICENSE.txt]: https://github.com/questrail/taffmat/blob/master/LICENSE.txt
[LX-10/20]: http://www.teac.co.jp/en/industry/measurement/datarecorder/lx10/index.html
[LX-110/120]: http://teac-ipd.com/data-recorders/lx-110120/
[numpy]: http://www.numpy.org
[PEP 740]: https://peps.python.org/pep-0740/
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: https://img.shields.io/pypi/v/taffmat.svg
[pypi ver link]: https://pypi.python.org/pypi/taffmat/
[pyright]: https://microsoft.github.io/pyright/
[pyversions image]: https://img.shields.io/pypi/pyversions/taffmat.svg
[release workflow]: https://github.com/questrail/taffmat/blob/master/.github/workflows/release.yml
[releases]: https://github.com/questrail/taffmat/releases
[ruff]: https://docs.astral.sh/ruff/
[taffmat]: https://github.com/questrail/taffmat
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
[WX-7000 Series]: http://teac-ipd.com/wx-7000/

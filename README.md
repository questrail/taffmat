# taffmat

[![Build Status][travis image]][travis link]
[![PyPi Version][pypi ver image]][pypi ver link]

A Python module for reading and writing Teac TAFFmat files.

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

## Contributing

[taffmat][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [taffmat][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the brnach is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.

## License

[taffmat][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[es8]: http://teac-ipd.com/data-recorders/es8/
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/questrail/taffmat/blob/develop/LICENSE.txt
[LX-10/20]: http://www.teac.co.jp/en/industry/measurement/datarecorder/lx10/index.html
[LX-110/120]: http://teac-ipd.com/data-recorders/lx-110120/
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: https://badge.fury.io/py/taffmat.png
[pypi ver link]: http://badge.fury.io/py/taffmat
[scott chacon]: http://scottchacon.com/about.html
[taffmat]: https://github.com/questrail/taffmat
[travis image]: https://travis-ci.org/questrail/taffmat.png?branch=master
[travis link]: https://travis-ci.org/questrail/taffmat
[WX-7000 Series]: http://teac-ipd.com/wx-7000/

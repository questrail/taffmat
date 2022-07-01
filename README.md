# taffmat

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

A Python 3.4+ module for reading and writing Teac TAFFmat files.

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

### Development Setup Using pyenv

Use the following commands to create a Python 3.9.9 virtualenv using [pyenv][]
and [pyenv-virtualenv][], install the requirements in the virtualenv named
`taffmat`, and list the available [Invoke][] tasks.

```bash
$ pyenv virtualenv 3.9.9 taffmat
$ pyenv activate taffmat
$ pip install -r requirements.txt
$ inv -l
```


## License

[taffmat][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[coveralls image]: http://img.shields.io/coveralls/questrail/taffmat/master.svg
[coveralls link]: https://coveralls.io/r/questrail/taffmat
[es8]: http://teac-ipd.com/data-recorders/es8/
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[invoke]: https://www.pyinvoke.org/
[LICENSE.txt]: https://github.com/questrail/taffmat/blob/master/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/taffmat.svg
[LX-10/20]: http://www.teac.co.jp/en/industry/measurement/datarecorder/lx10/index.html
[LX-110/120]: http://teac-ipd.com/data-recorders/lx-110120/
[numpy]: http://www.numpy.org
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-install]: https://github.com/pyenv/pyenv#installation
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: http://img.shields.io/pypi/v/taffmat.svg
[pypi ver link]: https://pypi.python.org/pypi/taffmat/
[taffmat]: https://github.com/questrail/taffmat
[travis image]: http://img.shields.io/travis/questrail/taffmat/master.svg
[travis link]: https://travis-ci.org/questrail/taffmat
[WX-7000 Series]: http://teac-ipd.com/wx-7000/

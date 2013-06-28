# taffmat

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

* Teac [LX-10/20]
* Teac [LX-110/120]
* Teac [WX-7000 Series]
* Teac [es8]

## Installation

You can install [taffmat] either via the Python Package Index (PyPI) or
from source:

To install using pip:

    $ pip install taffmat

**Source:** https://github.com/questrail/taffmat

## Requirements

[taffmat] requires the following Python packages:

* `numpy`

## Contributing

[taffmat] is developed using [git-flow]---"git extensions to
provide high-level repository operations for [Vincent Driessen's branching
model][nvie-git]." To contribute, [install git-flow], fork [taffmat], and
then run:

  git clone git@github.com:<username>/taffmat.git
  cd taffmat
  git branch master origin/master
  git flow init -d
  git flow feature start <your_feature>

When you're done coding and commiting the changes for `your_feature`,
issue:

  git flow feature publish <your_feature>

Then open a pull request to `your_feature` branch.

## License

[taffmat] is release under the MIT license. Please see the [LICENSE.txt]
file for more information.

[LX-10/20]: http://www.teac.co.jp/en/industry/measurement/datarecorder/lx10/index.html
[LX-110/120]: http://teac-ipd.com/data-recorders/lx-110120/
[WX-7000 Series]: http://teac-ipd.com/data-recorders/wx-7000-series/
[es8]: http://teac-ipd.com/data-recorders/es8/
[taffmat]: https://github.com/questrail/applyaf
[LICENSE.txt]: https://github.com/questrail/applyaf/blob/develop/LICENSE.txt
[git-flow]: https://github.com/nvie/gitflow
[nvie-git]: http://nvie.com/posts/a-successful-git-branching-model/
[install git-flow]: https://github.com/nvie/gitflow/wiki/Installation

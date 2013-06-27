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

You can install taffmat either via the Python Package Index (PyPI) or
from source:

To install using pip:

    $ pip install taffmat

**Source:** https://github.com/questrail/taffmat

## Requirements

taffmat requires the following Python packages:

* `numpy`


[LX-10/20]: http://www.teac.co.jp/en/industry/measurement/datarecorder/lx10/index.html
[LX-110/120]: http://teac-ipd.com/data-recorders/lx-110120/
[WX-7000 Series]: http://teac-ipd.com/data-recorders/wx-7000-series/
[es8]: http://teac-ipd.com/data-recorders/es8/

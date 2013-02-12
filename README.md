# taffmat

A Python module for reading and writing Teac TAFFmat files.

## About the TAFFmat file format

TAFFmat is Teac's proprietary file format used to store data from their
LX series and other data recorders, such as the LX-10.

According to the Teac "LX Series Recording Unit Instruction Manual":

>  TAFFmat (an acronym for Teac Data Acquisition File Format) is a
>  file format composed of the following:
>
>  * a data file containing A/D (analog to digital) converted data. The
>    file is binary format with the extension dat.
>  * a header file containing information such as recording
>    conditions. The file is in text format with the extension hdr. 

TAFFmat is a trademark of Teac Corporation.

## Installation

You can install taffmat either via the Python Package Index (PyPI) or
from source:

To install using pip:

    $ pip install taffmat

**Source:** https://github.com/questrail/taffmat

## Requirements

taffmat requires the following Python packages:

* `numpy`

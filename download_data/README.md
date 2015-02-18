This script downloads data from the pressureNet data API.
###Usage
1. In `config.py`, fill in your API key and the parameters (starting and ending timestamps and format) for the data you want to download.  See `config.example` for formatting.

2. `$ python download.py

You may optionally specify the name of the subdirectory you want the data to be stored in, like so: 

`$ python download.py my_subdirectory`

(the resulting JSON or CSV files would be saved in `data/my_subdirectory` or `conditions/my_subdirectory` depending on the API accessed).

If a subdirectory name is not specified then the script will generate one from the current date and time (eg. `data/2014-05-29T16:33:20.748169+00:00` or `conditions/2014-05-29T16:33:20.748169+00:00`).

Any failed API calls will be recorded in a file called error\_log in the same subdirectory as the JSON files.
###Requirements
[requests](http://docs.python-requests.org/en/latest/)

[arrow](https://crate.io/packages/arrow/0.4.4#description)

[tz\_local](https://pypi.python.org/pypi/tzlocal)

####Installing Python Packages
[Pip](https://pip.pypa.io/en/latest/) is the best tool for installing Python packages.  If you don't have Pip installed, you can do so from the command line with the following commands:
`wget https://bootstrap.pypa.io/get-pip.py`
`sudo python get-pip.py`

Otherwise you can manually download the packages from the links given above, find the `setup.py` script and run `sudo python setup.py install` to install the package.

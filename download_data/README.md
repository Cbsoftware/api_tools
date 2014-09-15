This script downloads JSON data from the pressureNet data and current conditions APIs.
###Usage
1. In `config.py`, fill in your API key and the parameters (dates, longitude, latitude) for the data you want to download.  See `config.example` for formatting.

2. `$ python download.py <name of service>`

Where <name of service> is either "conditions" (to access the current conditions API) or "readings" (to access the PressureNet Data API).

You may optionally specify the name of the subdirectory you want the data to be stored in, like so: 

`$ python download.py <name of service> my_subdirectory`

(the resulting JSON files would be saved in `data/my_subdirectory` or `conditions/my_subdirectory` depending on the API accessed).

If a subdirectory name is not specified then the script will generate one from the current date and time (eg. `data/2014-05-29T16:33:20.748169+00:00` or `conditions/2014-05-29T16:33:20.748169+00:00`).

Any failed API calls will be recorded in a file called error\_log in the same subdirectory as the JSON files.
###Requirements
[requests](https://github.com/kennethreitz/requests)

[arrow](http://crsmithdev.com/arrow/)

[tz\_local](https://pypi.python.org/pypi/tzlocal)

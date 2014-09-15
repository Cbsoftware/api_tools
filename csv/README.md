This script converts JSON files to CSV files.

The first line of the resulting CSV file will contain the keys/column names.

###Usage

`ruby json_to_csv.rb <name of json file>`

for example:

`ruby json_to_csv.rb gta_july.json`

or

`ruby json_to_csv.rb <name of json file> <name of csv file to create>`

for example:

`ruby json_to_csv.rb gta_july.json GTA_07_2013.csv`

If the name of the resulting CSV file is not specified then the script will create a file with the same name as the original JSON file (replacing the .json extension with .csv).

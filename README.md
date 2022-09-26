# ago_example_request
This module requests all of the data from an ArcGIS Online REST API service then downloads it locally as a CSV file; the default is `TRADE_LICENSES_PWD.csv`. It also can convert any columns from esriFieldTypeDate to a human-readable date; the default conversions for TRADE_LICENSES_PWD are `('REQUEST_DATE', 'ISSUEDATE', 'EXPIRATIONDATE')`. 

The script first requests an AGO token, then uses that token to download the relevant data. **It requires a username and password with sufficient privileges to receive a token (standard AGO accounts authenticated through AD likely will not work).** In addition, generating the AGO token requires you to be on the VPN or City network. 

Besides Python3, this script also requires the modules `click`, `requests`, and `pandas`. If you have pip, you can run `pip install click requests pandas`. Other package managers such as Conda exist and would suffice for installing these packages as well. 

## Get this script: 
* Basic Users: 
    * Copy and save the file `request_ago_api.py`
* Advanced Users: 
    * Clone this repository 

## Run this script: 
* Open PowerShell (Windows) or a Bash terminal (linux)
* Change your directory to wherever you downloaded the script by using the command `cd directory/sub_directory/sub_directory`
* (For the first-time only) run `pip install click requests pandas`
    * If you don't have pip, follow the system prompts to get pip or use your standard Python package manager to install the packages
* For the default TRADE_LICENSES_PWD, run `python request_ago_api.py --username=<username> --password=<password>`
    * Do not include "<" and ">"

### Notes
* The `--username` and `--password` command-line arguments are mandatory
* You can type `python request_ago_api.py -h` to access the help file for this script
* Use tab completion when working in PowerShell or Bash to ensure the correct names of directories and files 
* If you have another method of running python files, that should work fine as long as you can pass the command-line arguments 
* Downloading the data will overwrite the local file if it already exists 
* Any values that include spaces must be surrounded by 'single quotes'
* The `InsecureRequestWarning` can be ignored. 

### Advanced / For Other AGO Datasets
* An advanced user can input a different URL and filename (and username and password if necessary) to access other AGO resources that utilize the same process and new column names to convert from esriFieldTypeDate to human-readable dates by passing them as command line arguments.
    * `--url=<url>` - Must include the `http://`
    * `--filename=<filename>` - Must include the `.csv` 
        * Note that if a url different from the default url is passed, the filename parameter must also be passed. 
    * `-d <col_name>` or `--date_col=<col_name>` - Convert the subsequent column from "esriFieldTypeDate" to a human-readable date. 
        * This option must be included for each column that should be interpreted as a date. 
        * Leaving this option blank will avoid coercing any columns. 
* The url must point directly to the Layer or Table, not to the FeatureServer itself. 
    * Should have this format: 
        * `https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/<Dataset>/FeatureServer/0/query`
    * Not this format: 
        * `https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/<Dataset>/FeatureServer/query`
* The `requirements.txt` file marks the package versions needed and can be used to create a virtual environment. 
* If attempting to verify the query online, to access the AGO query operation you will need to access the url that begins with `services.arcgis.com` and not `phl.maps.arcgis.com`. This can be done by right-clicking on `Query` after logging in and opening that link in a new tab. 

## Examples: 
* Default / Minimum Necessary to run for _TRADE_LICENSES_PWD_:
    * `python request_ago_api.py --username=<username> --password=<password>`
* Advanced / For Other AGO Datasets: 
    * `python request_ago_api.py --username=<username> --password=<password> --url=<new_url> --filename=<filename.csv> -d <col_name_1> -d <col_name_2>`
    * This is not guaranteed to work on all City datasets. At a minimum, any dataset must have integer object ID field. 
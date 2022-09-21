# ago_example_request
This module requests all of the data from an ArcGIS Online REST API service and then downloads it locally as a CSV file; the default is `TRADE_LICENSES_PWD.csv`. 

The script first requests an AGO token, then uses that token to download the relevant data. **It requires a username and password with sufficient privileges to receive a token (standard AGO accounts authenticated through AD likely will not work).** 

Besides Python3, this script also requires the modules `click`, `requests`, and `pandas`. If you have pip, you can run `pip install click requests pandas`. Other package managers such as Conda exist and would suffice for installing these packages as well. 

## Get this script: 
* Basic Users: 
    * Download the file `request_ago_api.py`
* Advanced Users (if you have access to the City of Philadelphia GitHub organization)
    * Clone this repository 

## Run this script: 
* Open PowerShell (Windows) or a Bash terminal (linux)
* Change your directory to wherever you downloaded the script by using the command `cd directory/sub_directory/sub_directory`
* (For the first-time only) run `pip install click requests pandas`
    * If you don't have pip, follow the system prompts to get pip
* Run `python request_ago_api.py --username=<username> --password=<password>`
### Notes
* The `--username` and `--password` command-line arguments are mandatory
* Use tab completion when working in PowerShell or Bash to ensure the correct names of directories and files 
* If you have another method of running python files, that should work fine as long as you can pass the mandatory command-line arguments 
* Downloading the data will overwrite the local file if it already exists. 
* An advanced user can input a different URL and filename (and username and password if necessary) to access other AGO resources that utilize the same process by also passing them as command line arguments.
    * `--url=<url>` - Must include the `http://`
    * `--filename=<filename>` - Must include the `.csv`
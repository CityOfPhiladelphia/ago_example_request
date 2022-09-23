import requests
import click
import pandas as pd
import time
import os

DEFAULT_URL = 'https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/TRADE_LICENSES_PWD/FeatureServer/0/query'
DEFAULT_FILENAME = 'TRADE_LICENSES_PWD.csv'
DEFAULT_DATE_COLS = ('REQUEST_DATE', 'ISSUEDATE', 'EXPIRATIONDATE')

def generateToken(username, password):
    """
    Generate Token generates an access token in exchange for \
    user credentials that can be used by clients when working with the ArcGIS Portal API:
    https://developers.arcgis.com/rest/users-groups-and-items/generate-token.htm
    """
    url = 'https://arcgis.com/sharing/rest/generateToken'
    data = {'username': username,
            'password': password,
            'referer': 'https://www.arcgis.com',
            'f': 'json'}
    rv = requests.post(url, data, verify=False).json()
    try:
        return rv['token']
    except:  
        try: 
            rv['error']
            print(f'JSON return value: {rv}')
            print('Token not found')
            quit()
        except Exception as e: 
            print('Unknown exception raised')
            print(e)
            quit()

def get_data(url, params, data_designation):
    '''
    Gets data from specified URL and JSON decodes
    '''
    r = requests.get(url, params=params)
    if r.status_code != 200:
        raise Exception(f'Status Code: {r.status_code} - Reason: {r.reason}')
    try:
        text = r.json()
        return text[data_designation]
    except requests.exceptions.JSONDecodeError:
        print(f'Text: {r.text}')
        raise Exception('json module unable to decode text')
    except KeyError: # Checks for no data
        raise KeyError(text)

def pull_data(url, token, filename, date_cols): 
    '''
    Successively calls get_data() for the max number of records allowed in each data pull
    '''
    print('Gathering Records')
    x = -1
    start = time.time()
    while True:
        params = {
            'where': f'OBJECTID > {x}',
            'outFields': '*', 
            'token': token, 
            'f': 'pjson'
            }
        rv_text = get_data(url, params, 'features')
        if rv_text == []: 
            break
        
        data = pd.json_normalize(rv_text)
        data.columns = data.columns.str.removeprefix('attributes.')
        for col in date_cols: 
            try: 
                if pd.api.types.is_integer_dtype(data[col]): 
                    try: 
                        data[col] = pd.to_datetime(data[col], unit='ms')
                    except Exception as e: 
                        print(f'    Unable to coerce column "{col}" to datetime')
                else: 
                    print(f'    Unable to coerce column "{col}" to datetime')
            except KeyError as e: 
                raise KeyError(f'{e} is not a named column in dataset')
        if x == -1: 
            if date_cols != (): 
                print()
                print(f'Coercing the following columns to datetime format:\n{date_cols}')
            data.to_csv(filename, index=False, mode='w')
        else: 
            data.to_csv(filename, index=False, mode='a')
        x = data['OBJECTID'].max()
        print(f'    Record Number: {x}')
        
    end = time.time()

    print(f'Serial Data API pull required {round(end - start, 0)} seconds')
    
@click.command()
@click.option('--username', help='ArcGIS username login with admin access')
@click.option('--password', help='Account password')
@click.option('--url', default=DEFAULT_URL, show_default=True, 
    help='URL of ArcGIS Resource to access - defaults to URL posted at the top of this script')
@click.option('--filename', default=DEFAULT_FILENAME, show_default=True, 
    help='Name of CSV file to create with exported data')
@click.option('--date_col', '-d', multiple=True, default=DEFAULT_DATE_COLS, show_default=True, 
    help='A data column of type "esriFieldTypeDate" that should be converted to human-readable datetimes. Must be written in form "-d col_1 -d col_2 -d col_3" etc.')
def main(username, password, url, filename, date_col): 
    '''
    \b
    This module gets all of the data from an ArcGIS Online REST API service; the 
    default is TRADE_LICENSES_PWD. The script first requests an AGO token, then 
    uses that token to download the relevant data. 
    
    This script requires a username and password with sufficient privileges to 
    receive a token (standard AGO accounts authenticated through AD likely will not work). 
    
    An advanced user can 
    1. Input a different URL and filename (and username and password 
    if necessary) to access other AGO resources that utilize the same process by passing 
    them as command line arguments. 
    2. Specify for that URL and filename which columns should be converted from "esriFieldTypeDate"
    to human-readable datetimes. 
    '''
    if url != DEFAULT_URL: 
        if filename == DEFAULT_FILENAME: 
            raise ValueError(f'Custom URL presented, but filename remains "{DEFAULT_FILENAME}"')
        if date_col == DEFAULT_DATE_COLS: 
            date_col = ()
    token = generateToken(username, password)
    pull_data(url, token, filename, date_col)
    print(f'Script completed - file saved to {os.getcwd()}\\{filename}')

if __name__ == '__main__': 
    main()
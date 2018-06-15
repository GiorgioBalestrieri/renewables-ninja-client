import requests
import pandas as pd
import os
from pathlib import Path
import json

TOKEN_FILENAME = 'ninja_token.json'
API_BASE = 'https://www.renewables.ninja/api/'

def _get_path_to_module():
    '''Get path to this module.'''
    return Path(os.path.realpath(__file__)).parent

def _load_token():
    '''Load token.'''
    path_to_dir = _get_path_to_module()
    with open(path_to_dir / TOKEN_FILENAME, 'r') as f:
        return json.load(f)['token']

def query_pv(lat, lon, date_from, date_to, 
             tilt, azim=180, tracking=0, system_loss=10, 
             capacity=1, dataset='merra2', interpolate=False, 
             local_time=False, metadata=False, raw=False):

    s = requests.session()

    # get token
    token = _load_token()
    
    # send token through header
    s.headers = {'Authorization': 'Token ' + token}
    
    url = API_BASE + 'data/pv'
    
    # pre-process inputs
    date_from = _date_to_string(date_from)
    date_to   = _date_to_string(date_to)

    args = {
        'lat': lat,
        'lon': lon,
        'date_from': date_from,
        'date_to': date_to,
        'dataset': dataset,
        'capacity': capacity,
        'system_loss': system_loss,
        'tracking': tracking,
        'tilt': tilt,
        'azim': azim,
        'format': 'json',
        'metadata': metadata,
        'raw': raw
    }

    r = s.get(url, params=args)
    
    if not r.ok:
        raise Exception('Query failed. Check input parameters.')

    # Parse JSON to get a pandas.DataFrame
    return pd.read_json(r.text, orient='index')

def query_wind(lat, lon, date_from, date_to,
               height, capacity=1, turbine='Vestas V80 2000',
               metadata=False, raw=False):

    s = requests.session()
    
   # get token
    token = _load_token()

    # Send token header with each request
    s.headers = {'Authorization': 'Token ' + TOKEN}
    
    url = API_BASE + 'data/wind'
    
    # pre-process inputs
    date_from = _date_to_string(date_from)
    date_to   = _date_to_string(date_to)

    args = {
        'lat': lat,
        'lon': lon,
        'date_from': date_from,
        'date_to': date_to,
        'capacity': capacity,
        'height': height,
        'turbine': turbine,
        'format': 'json',
        'metadata': metadata,
        'raw': raw
    }

    r = s.get(url, params=args)
    
    if not r.ok:
        raise Exception('Query failed. Check input parameters.')
    
    # Parse JSON to get a pandas.DataFrame
    return pd.read_json(r.text, orient='index')

def _date_to_string(date, date_format='%Y-%m-%d'):
    
    if isinstance(date, str):
        return date
    elif isinstance(date, pd.datetime):
        return date.strftime(date_format)
    else:
        raise Exception('input date must be str or pd.datetime, not {}'.format(type(date)))
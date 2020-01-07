import requests
import pandas as pd
import datetime as dt
from pathlib import Path
import os
import json
from dataclasses import dataclass

from typing import Dict, Union

API_BASE_URL = "https://www.renewables.ninja/api"
PV_URL = f"{API_BASE_URL}/data/pv"
WIND_URL = f"{API_BASE_URL}/data/wind"

DATE_FORMAT = "%Y-%m-%d"

TOKEN_FILENAME = 'ninja_token.json'


@dataclass(frozen=True)
class Client:
    token: str
    pv_url: str = PV_URL
    wind_url: str = WIND_URL

    @classmethod
    def from_file(cls, path=None, filename: str = TOKEN_FILENAME):
        if path is None:
            path = _get_path_to_module()
        return cls(_load_token(path / filename))


def get_headers(client: Client) -> Dict[str, str]:
    return {'Authorization': 'Token ' + client.token}


def date_to_str(date: Union[dt.date,dt.datetime], date_format:str=DATE_FORMAT) -> str:
    return date.strftime(date_format)


def _get_path_to_module():
    '''Get path to this module.'''
    return Path(os.path.realpath(__file__)).parent


def _load_token(filename):
    '''Load token.'''
    with open(filename, 'r') as f:
        return json.load(f)['token']

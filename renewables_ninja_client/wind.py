import requests
import pandas as pd
import datetime as dt
from io import StringIO

from typing import Dict, Union

from .utils import Client, get_headers, date_to_str

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def query_wind(
    client: Client,
    date_from: Union[dt.date, dt.datetime], 
    date_to: Union[dt.date, dt.datetime], 
    lat: float,
    lon: float, 
    height: float, 
    capacity: float = 1., 
    turbine='Vestas V80 2000', 
    interpolate: bool = False, 
    local_time: bool = False, 
    raw: bool = False,
    ) -> pd.DataFrame:

    headers = get_headers(client)
    date_from = date_to_str(date_from)
    date_to   = date_to_str(date_to)

    params = {
        'date_from': date_from,
        'date_to': date_to,
        'lat': lat,
        'lon': lon,
        'height': height,
        'capacity': capacity,
        'turbine': turbine,
        'raw': raw,
        'interpolate': interpolate,
        'local_time': local_time,
        'format': 'csv',
        'header': False,
    }

    r = requests.get(client.wind_url, params=params, headers=headers)

    if not r.ok:
        logger.error("Query failed with status {}: {}".format(r.status_code, r.text))
        r.raise_for_status()
    return pd.read_csv(StringIO(r.text), index_col=0)
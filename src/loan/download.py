import requests
import pandas as pd

from io import StringIO
from datetime import datetime


def government_borrowing_rate():
    """Download historical Swedish government borrowing rate.

    Download historical government borrowing rates from the Swedish National
    Debt Office.

    Returns:
        A pandas data frame.
    """
    url = "https://www.riksgalden.se/globalassets/dokument_sve/statslaneranta/slr-historisk-statslaneranta-csv.csv"
    request = requests.get(url)
    if request.status_code == 200:
        decimal_periods = request.text.replace(",", ".")
        data_string = StringIO(decimal_periods)
        return_df = pd.read_csv(data_string, delimiter=";", parse_dates=["Datum"])
        return return_df
    else:
        raise ConnectionError(
            f"The connection to {url} got a status code of {request.status_code}, instead of status code 200."
        )


def consumer_price_index():
    """Download historical Swedish consumer price index.

    Download historical comnusmer price index data from Statistics Sweden.

    Returns:
        A pandas data frame.
    """
    url = "https://api.scb.se/OV0104/v1/doris/sv/ssd/START/PR/PR0101/PR0101A/KPItotM"
    query = {
        "query": [
            {
                "code": "ContentsCode",
                "selection": {"filter": "item", "values": ["000004VU"]},
            }
        ],
        "response": {"format": "csv3"},
    }
    request = requests.post(url, json=query)
    if request.status_code == 200:
        data_string = StringIO(request.text)
        return_df = (
            pd.read_csv(data_string)
            .drop(["ContentsCode"], axis=1)
            .rename(columns={"Tid": "date", "TAB5737": "consumer_price_index"})
        )
        return_df["date"] = return_df["date"].str.replace(
            r"M(\d+)", r"-\1-01", regex=True
        )
        return_df["date"] = pd.to_datetime(return_df["date"])
        return return_df
    else:
        raise ConnectionError(
            f"The connection to {url} got a status code of {request.status_code}, instead of status code 200."
        )


def policy_rate():
    url = f"https://api.riksbank.se/swea/v1/Observations/SECBREPOEFF/1994-06-01/{datetime.now().strftime('%Y-%m-%d')}"
    request = requests.get(url)
    if request.status_code == 200:
        string_data = StringIO(request.text)
        return_df = pd.read_json(string_data)
        return_df = return_df.rename(columns={"value": "policy_rate"})
        return return_df
    else:
        raise ConnectionError(
            f"The connection to {url} got a status code of {request.status_code}, instead of status code 200."
        )

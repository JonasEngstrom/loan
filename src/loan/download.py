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
    """Download historical Swedish policy rates.

    Download historical policy rates from the Swedish National Bank.

    Returns:
        A pandas data frame.
    """
    series_id = "SECBREPOEFF"
    start_date = "1994-06-01"
    end_date = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.riksbank.se/swea/v1/Observations/{series_id}/{start_date}/{end_date}"
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


def omxs30():
    """Download historical OMXS30 index data.

    Donwload historical data on the OMX Stockholm 30 index from Nasdaq.

    Returns:
        A pandas data frame.
    """
    today = datetime.now()
    instrument = "SE0000337842"
    start_date = today.replace(year=today.year - 10).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")
    url = f"https://api.nasdaq.com/api/nordic/instruments/{instrument}/chart/download?assetClass=INDEXES&fromDate={start_date}&toDate={end_date}"
    headers = {"User-Agent": "Mozilla/5.0"}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        json_data = request.json().get("data", {}).get("charts", {}).get("rows", {})
        return_df = pd.DataFrame(json_data).replace(",", "", regex=True)
        numeric_columns = return_df.columns.drop(["dateTime"])
        return_df[numeric_columns] = return_df[numeric_columns].apply(pd.to_numeric)
        return_df["dateTime"] = pd.to_datetime(return_df["dateTime"])
        return_df = return_df.rename(
            columns={"dateTime": "date", "totalVolume": "total_volume"}
        )
        return return_df
    else:
        raise ConnectionError(
            f"The connection to {url} got a status code of {request.status_code}, instead of status code 200."
        )

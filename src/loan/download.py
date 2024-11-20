import requests
import pandas as pd

from io import StringIO


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

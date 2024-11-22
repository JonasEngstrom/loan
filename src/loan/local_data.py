import pandas as pd

from importlib.resources import files


def old_omxs30_data():
    """Load the file old_omxs30_data.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("old_omxs30_data.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return_df = return_df.rename(
        columns={
            "high_price": "high",
            "low_price": "low",
            "closing_price": "close",
            "average_price": "average",
        }
    )
    return return_df


def local_government_borrowing_rate():
    """Load the file government_borrowing_rate.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("government_borrowing_rate.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return return_df


def local_consumer_price_index():
    """Load the file consumer_price_index.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("consumer_price_index.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return return_df


def local_policy_rate():
    """Load the file policy_rate.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("policy_rate.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return return_df


def local_omxs30():
    """Load the file omxs30.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("omxs30.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return return_df


def local_list_rates():
    """Load the file list_rates.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("list_rates.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return return_df

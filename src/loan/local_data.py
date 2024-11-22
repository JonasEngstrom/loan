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


def local_complete_omxs30():
    """Merge data from old_omxs30() and local_omxs30.

    Return:
        A pandas data frame.
    """
    old_omxs30 = old_omxs30_data()
    new_omxs30 = local_omxs30()
    return_df = (
        pd.concat([old_omxs30, new_omxs30[old_omxs30.columns.values]])
        .drop_duplicates()
        .sort_values("date")
    )
    return return_df


def local_merged_table() -> None:
    """Return a table of merged historic datat.

    Merge data on consumer price index, government borrowing rate, OMXS30
    index, and policy rate in one table. Remove incomplete cases and fill NaN
    values forward.

    Returns:
        A pandas data frame.
    """
    loading_functions = [
        local_government_borrowing_rate,
        local_complete_omxs30,
        local_policy_rate,
    ]
    data_frame_list = [i() for i in loading_functions]
    all_dates = pd.concat([i["date"] for i in data_frame_list])
    start_date = min(all_dates)
    end_date = max(all_dates)
    return_df = pd.DataFrame({"date": pd.date_range(start_date, end_date)})
    for i in data_frame_list:
        return_df = pd.merge(return_df, i, how="left")
    return_df = return_df[
        [
            "date",
            "government_borrowing_rate",
            "close",
            "policy_rate",
        ]
    ]
    return_df = (
        return_df.rename(columns={"close": "omxs30"})
        .sort_values("date")
        .ffill()
        .dropna()
    )
    return return_df

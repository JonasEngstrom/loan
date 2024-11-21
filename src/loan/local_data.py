import pandas as pd

from importlib.resources import files


def old_omxs30_data():
    """Load the file old_omxs30_data.csv.

    Returns:
        A pandas data frame.
    """
    data_path = files("src.loan.data").joinpath("old_omxs30_data.csv")
    return_df = pd.read_csv(data_path, parse_dates=["date"])
    return return_df

import pandas as pd

from src.loan import local_data

from datetime import datetime, date


class HistoricTables:
    """Class for formatting historic finance tables."""

    # Minimum standard rate (swe: schablonintäkt) in percent.
    _minimum_standard_rate = 0.0125

    @classmethod
    def _calculate_rate_of_change(
        cls, start_value: float, end_value: float, time_delta: float
    ) -> float:
        """Calculate rate of change as a geometric mean.

        Calculates the rate of change between two values per unit of time.
        Uses the formula (end_value / start_value) ** (1 / time_delta).
        In reality a - 1 should be added at the end to calculate rate of change
        but this was omitted to simplify further calculations usning the rate.

        Args:
            start_value: Start value.
            end_value: End value.
            time_delta: Time between start_value and end_value in time units.
        """
        return (end_value / start_value) ** (1 / time_delta)

    @classmethod
    def _expand_date_range(cls, data_frame) -> pd.DataFrame:
        """Expand pandas date range and forward fill.

        Args:
            data_frame: A pandas data frame with a column named date.

        Returns:
            A pandas data frame.
        """
        return_df = (
            pd.DataFrame(
                {
                    "date": pd.date_range(
                        min(data_frame["date"]), max(data_frame["date"])
                    )
                }
            )
            .merge(data_frame, how="left")
            .ffill()
        )
        return return_df

    def __init__(
        self,
        new_omxs30=local_data.local_omxs30(),
        goverment_borrowing_rate=local_data.local_government_borrowing_rate(),
        consumer_price_index=local_data.local_consumer_price_index(),
        policy_rate=local_data.local_policy_rate(),
        old_omxs30=local_data.old_omxs30_data(),
    ) -> None:
        """Initialized HistoricTables object.

        Args:
            new_omxs30: Pandas data frame from download.omxs30 or
                local_data.local_omxs30.
            goverment_borrowing_rate: Pandas data frame from
                download.government_borrowing_rate or
                local_data.local_government_borrowing_rate.
            consumer_price_index: Pandas data frame from
                download.consumer_price_index or
                local_data.local_consumer_price_index.
            policy_rate: Pandas data frame from download.policy_rate or
                local_data.policy_rate.
            old_omxs30: Pandas data frame from local_data.old_omxs30_data.
        """
        self._new_omxs30 = new_omxs30
        self._goverment_borrowing_rate = goverment_borrowing_rate
        self._consumer_price_index = consumer_price_index
        self._policy_rate = policy_rate
        self._old_omxs30 = old_omxs30

    @property
    def omxs30(self) -> pd.DataFrame:
        """Merges old and new omxs30 data.

        Returns:
            A pandas data frame.
        """
        old_omxs30_last_date = self._old_omxs30["date"].max()
        new_omxs30_data = self._new_omxs30.query("date > @old_omxs30_last_date")[
            self._old_omxs30.columns
        ]
        return_df = (
            pd.concat([self._old_omxs30, new_omxs30_data])
            .sort_values("date")
            .reset_index(drop=True)
            .rename(columns={"close": "omxs30"})
            .drop(["high", "low", "average", "total_volume", "turnover"], axis=1)
        )
        return_df = self._expand_date_range(return_df)
        return_df["omxs30_change_multiplier"] = (
            return_df["omxs30"].shift(-1) / return_df["omxs30"]
        )
        return_df = return_df.drop(["omxs30"], axis=1).dropna()
        return return_df

    @property
    def government_borrowing_rate(self) -> pd.DataFrame:
        """Formats government borrowing rate table."""
        return_df = (
            self._goverment_borrowing_rate.drop(["current_year_average"], axis=1)
            .sort_values("date")
            .reset_index(drop=True)
        )
        return_df.loc[:, ("government_borrowing_rate")] = (
            return_df["government_borrowing_rate"] / 100
        )
        return return_df

    @property
    def standard_rate(self) -> pd.DataFrame:
        """Calculate standard rate (swe: schablonintäkt).

        Calculates the standard rate (swe: schablonintäkt) to be used for
        calculating the capital gains tax (swe: avkastningsskatt) for each date
        during a year.

        See: https://www.avanza.se/lar-dig-mer/avanza-akademin/skatt-deklaration/hur-beskattas-en-kapitalforsakring.html
        for details on how the calculation is performed.

        Returns:
            A pandas data frame.
        """
        return_df = HistoricTables._expand_date_range(self.government_borrowing_rate)
        return_df["standard_rate"] = (
            return_df["government_borrowing_rate"].shift(1) + 0.01
        ).apply(
            lambda x: (
                self._minimum_standard_rate if x < self._minimum_standard_rate else x
            )
        )
        return_df["date"] = return_df.loc[
            (return_df["date"].dt.month == 11) & (return_df["date"].dt.day == 30),
            ("date"),
        ].apply(lambda x: x.replace(year=x.year + 1, month=1, day=1))
        return_df = return_df.drop(["government_borrowing_rate"], axis=1).dropna()
        max_date = return_df.loc[return_df["date"] == return_df["date"].max(), :]
        max_date.loc[:, ("date")] = max_date.loc[:, ("date")].apply(
            lambda x: datetime(year=x.year, month=12, day=31)
        )
        return_df = pd.concat([return_df, max_date])
        return_df = self._expand_date_range(return_df).reset_index(drop=True)
        return_df.loc[return_df["date"].dt.month > 6, ("standard_rate")] = (
            return_df["standard_rate"] / 2
        )
        return return_df

    @property
    def consumer_price_index(self) -> pd.DataFrame:
        """Formats consumer price index."""
        return_df = self._consumer_price_index.sort_values("date").reset_index(
            drop=True
        )
        return_df["time_delta"] = (
            return_df["date"].shift(-1) - return_df["date"]
        ).apply(lambda x: x.days)
        return_df["consumer_price_index_change_multiplier"] = (
            self._calculate_rate_of_change(
                return_df["consumer_price_index"],
                return_df["consumer_price_index"].shift(-1),
                return_df["time_delta"],
            )
        )
        return_df = return_df.drop(
            ["time_delta", "consumer_price_index"], axis=1
        ).dropna()
        return return_df

    @property
    def policy_rate(self) -> pd.DataFrame:
        """Formats policy rate."""
        return_df = self._policy_rate.sort_values("date").reset_index(drop=True)
        return_df.loc[:, ("policy_rate")] = return_df["policy_rate"] / 100
        return return_df

    @property
    def main_table(self) -> pd.DataFrame:
        """Return table with change multipliers.

        Return a table of OMXS30, policy_rate, standard_rate, and consumer
        price index change multipliers, that can be used for time series
        calculations.

        Returns:
            A pandas data frame.
        """
        now = self.omxs30.date.max()
        return_df = (
            pd.merge(
                pd.merge(
                    pd.merge(
                        pd.merge(
                            self._min_max_date_range(),
                            self.omxs30,
                            how="left",
                            on="date",
                        ),
                        self.policy_rate,
                        how="left",
                        on="date",
                    ),
                    self.standard_rate,
                    how="left",
                    on="date",
                ),
                self.consumer_price_index,
                how="left",
                on="date",
            )
            .ffill()
            .dropna()
            .query("date < @now")
            .sort_values("date")
            .reset_index(drop=True)
        )
        return return_df

    def _min_max_date_range(self) -> tuple:
        """Return a range between min and max dates in class input data frames.

        Returns:
            A pandas data frame.
        """
        dataframes_to_check = [
            self.consumer_price_index,
            self.standard_rate,
            self.omxs30,
        ]
        min_max_dates = pd.concat([i["date"] for i in dataframes_to_check])
        min_max_range = pd.date_range(min_max_dates.min(), min_max_dates.max())
        return_df = pd.DataFrame({"date": min_max_range})
        return return_df

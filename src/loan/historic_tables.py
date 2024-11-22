import pandas as pd

from src.loan import local_data


class HistoricTables:
    """Class for formatting historic finance tables."""

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
    def omxs30(self):
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
        return return_df

    @property
    def government_borrowing_rate(self):
        """Formats governemnt borrowing rate table."""
        return_df = (
            self._goverment_borrowing_rate.drop(["current_year_average"], axis=1)
            .sort_values("date")
            .reset_index(drop=True)
        )
        return return_df

    @property
    def consumer_price_index(self):
        """Formats consumer price index."""
        return_df = self._consumer_price_index.sort_values("date").reset_index(
            drop=True
        )
        return return_df

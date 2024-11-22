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
            new_omxs30: Pandas dataframe from download.omxs30 or
                local_data.local_omxs30.
            goverment_borrowing_rate: Pandas dataframe from
                download.government_borrowing_rate or
                local_data.local_government_borrowing_rate.
            consumer_price_index: Pandas dataframe from
                download.consumer_price_index or
                local_data.local_consumer_price_index.
            policy_rate: Pandas dataframe from download.policy_rate or
                local_data.policy_rate.
            old_omxs30: Pandas dataframe from local_data.old_omxs30_data.
        """
        self._new_omxs30 = new_omxs30
        self._goverment_borrowing_rate = goverment_borrowing_rate
        self._consumer_price_index = consumer_price_index
        self._policy_rate = policy_rate
        self._old_omxs30 = old_omxs30

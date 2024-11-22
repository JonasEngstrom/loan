import unittest

from src.loan.historic_tables import HistoricTables
from src.loan import local_data

import numpy as np


class TestHistoricTables(unittest.TestCase):
    """Test case for HistoricTables class."""

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)
        self.checker = HistoricTables()

    def test___init__(self) -> None:
        """Check that initialization works."""
        self.assertTrue(self.checker._new_omxs30.equals(local_data.local_omxs30()))
        self.assertTrue(
            self.checker._goverment_borrowing_rate.equals(
                local_data.local_government_borrowing_rate()
            )
        )
        self.assertTrue(
            self.checker._consumer_price_index.equals(
                local_data.local_consumer_price_index()
            )
        )
        self.assertTrue(
            self.checker._policy_rate.equals(local_data.local_policy_rate())
        )
        self.assertTrue(self.checker._old_omxs30.equals(local_data.old_omxs30_data()))

    def test_omxs30(self):
        """Test that omxs30 property works as expected."""
        self.assertEqual(self.checker.omxs30.iloc[0, 1], np.float64(125.00))

import unittest

from src.loan import local_data

import numpy as np
import pandas as pd


class TestLocalData(unittest.TestCase):
    """Test the functions in local_data.py."""

    def __init__(self, method_name: str = "runTest") -> None:
        """Initialize test class."""
        super().__init__(method_name)

    def test_old_omxs30_data(self) -> None:
        """Test that old_omxs30_data.csv loads as expected."""
        test_data = local_data.old_omxs30_data()
        self.assertEqual(test_data.iloc[0, 1], np.float64(2626.57))

    def test_local_government_borrowing_rate(self) -> None:
        """Test that government_borrowing_rate.csv loads as expected."""
        test_data = local_data.local_government_borrowing_rate()
        test_date = pd.to_datetime("2024-11-15")
        self.assertEqual(
            test_data.query("date == @test_date").iloc[0, 1], np.float64(2.11)
        )

    def test_local_consumer_price_index(self) -> None:
        """Test that consumer_price_index.csv loads as expected."""
        test_data = local_data.local_consumer_price_index()
        test_date = pd.to_datetime("2024-10-01")
        self.assertEqual(
            test_data.query("date == @test_date").iloc[0, 1], np.float64(415.51)
        )

    def test_local_policy_rate(self) -> None:
        """Test that policy_rate.csv loads as expected."""
        test_data = local_data.local_policy_rate()
        test_date = pd.to_datetime("2024-11-21")
        self.assertEqual(
            test_data.query("date == @test_date").iloc[0, 1], np.float64(2.75)
        )

    def test_omxs30(self) -> None:
        """Test that omxs30.csv loads as expected."""
        test_data = local_data.local_omxs30()
        test_date = pd.to_datetime("2024-11-20")
        self.assertEqual(
            test_data.query("date == @test_date").iloc[0, 3], np.float64(2508.29)
        )

    def test_list_rates(self) -> None:
        """Test that list_rates.csv loads as expected."""
        test_data = local_data.local_list_rates()
        self.assertEqual(test_data.iloc[0, 0], "Avanza Bank")

    def test_local_complete_omxs30(self) -> None:
        """Test that local_complete_omxs30 merges data as expected."""
        test_data = local_data.local_complete_omxs30()
        self.assertEqual(test_data.iloc[0, 1], np.float64(125.00))
        self.assertEqual(
            min(test_data["date"]), min(local_data.old_omxs30_data()["date"])
        )
        self.assertEqual(max(test_data["date"]), max(local_data.local_omxs30()["date"]))

    def test_local_merged_table(self) -> None:
        """Test that local_merged_table returns expected table."""
        test_data = local_data.local_merged_table()
        self.assertEqual(test_data.iloc[0, 1], np.float64(8.89))

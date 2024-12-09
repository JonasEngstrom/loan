import unittest

from src.loan.historic_tables import HistoricTables
from src.loan import local_data

import numpy as np
import pandas as pd

from datetime import datetime


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
        self.assertEqual(self.checker.omxs30.iloc[0, 1], np.float64(1.0074400000000001))

    def test_government_borrowing_rate(self):
        """Test that government_borrowing_rate property works as expected."""
        self.assertEqual(
            self.checker.government_borrowing_rate.iloc[0, 1], np.float64(0.1073)
        )

    def test_consumer_price_index(self):
        """Test that consumer_price_index property works as expected."""
        self.assertEqual(
            self.checker.consumer_price_index.iloc[0, 1], np.float64(1.000503907035366)
        )

    def test_policy_rate(self):
        """Test that policy_rate property works as expected."""
        self.assertEqual(self.checker.policy_rate.iloc[0, 1], np.float64(0.0695))

    def test__calculate_rate_of_change(self):
        start_value = 100
        end_value = 200
        time_delta = 4
        rate_of_change = self.checker._calculate_rate_of_change(
            start_value, end_value, time_delta
        )
        self.assertAlmostEqual(start_value * (rate_of_change) ** time_delta, end_value)

    def test_standard_rate(self):
        """Test that standard rate is calculated as expected."""
        tax_amount = (
            pd.merge(
                pd.DataFrame(
                    {
                        "date": [
                            datetime(2024, 1, 1),
                            datetime(2024, 2, 2),
                            datetime(2024, 7, 1),
                        ],
                        "amount": [2e5, 5e4, 5e4],
                    }
                ),
                self.checker.standard_rate,
                how="left",
            )
            .assign(standard_sum=lambda x: x.amount * x.standard_rate)
            .loc[:, ("standard_sum")]
            .sum()
            * 0.3
        )
        self.assertAlmostEqual(tax_amount, 2986.50)

    def test__min_max_date_range(self) -> None:
        """Test that _min_max_date_range returns correct dates."""
        test_data = self.checker._min_max_date_range()
        self.assertEqual(self.checker._min_max_date_range().min().dt.year.item(), 1980)
        self.assertEqual(self.checker._min_max_date_range().min().dt.month.item(), 1)
        self.assertEqual(self.checker._min_max_date_range().min().dt.day.item(), 1)
        self.assertEqual(self.checker._min_max_date_range().max().dt.year.item(), 2024)
        self.assertEqual(self.checker._min_max_date_range().max().dt.month.item(), 12)
        self.assertEqual(self.checker._min_max_date_range().max().dt.day.item(), 31)

    def test_main_table(self) -> None:
        """Test that main table is correctly formatted."""
        self.assertEqual(
            list(self.checker.main_table.columns),
            [
                "date",
                "omxs30_change_multiplier",
                "policy_rate",
                "standard_rate",
                "consumer_price_index_change_multiplier",
            ],
        )
        self.assertEqual(
            list(self.checker.main_table.iloc[0, 1:]),
            [
                np.float64(0.9963649197106051),
                np.float64(0.0695),
                np.float64(0.08539999999999999),
                np.float64(1.0),
            ],
        )

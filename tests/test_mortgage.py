import unittest

from src.loan import mortgage

from datetime import datetime, date
import numpy as np
import pandas as pd


class TestMortgage(unittest.TestCase):
    """Test case for Mortgage class."""

    def __init__(self, method_name: str = "runTest") -> None:
        """Set up test case for Mortgage class."""
        super().__init__(method_name)
        self.checker = mortgage.Mortgage(
            asset_value=10e6,
            birth_date="2006-09-02",
            household_gross_income=2e6,
            principal=5e6,
            payoff_time=25,
            interest_markup=1e-2,
            days_offset=0,
            fraction_invested=0.5,
        )

    def test___init__(self) -> None:
        """Check that __init__ exhibits expected behavior."""
        self.assertEqual(self.checker.asset_value, 10e6)
        self.assertIsInstance(self.checker.birth_date, date)
        self.assertEqual(self.checker.birth_date.year, 2006)
        self.assertEqual(self.checker.birth_date.month, 9)
        self.assertEqual(self.checker.birth_date.day, 2)
        self.assertEqual(self.checker.household_gross_income, 2e6)
        self.assertEqual(self.checker.initial_principal, 5e6)
        self.assertEqual(self.checker.principal, 5e6)
        self.assertEqual(
            self.checker.omxs30_change_multiplier[0], np.float64(0.9963649197106051)
        )
        self.assertEqual(self.checker.bank_rate[0], np.float64(1.0002096054462695))
        self.assertEqual(self.checker.standard_rate[0], np.float64(0.08539999999999999))
        self.assertEqual(
            self.checker.historic_date_range[0],
            np.datetime64("1994-06-01T00:00:00.000000000"),
        )
        self.assertEqual(self.checker.days_offset, 0)
        self.assertEqual(self.checker.payoff_time, 25)

    def test_loan_to_value_ratio(self) -> None:
        """Check that loan-to-value ratio calculates correctly."""
        self.assertEqual(self.checker.loan_to_value_ratio, 0.5)

    def test_debt_ratio(self) -> None:
        """Check that debt ratio calculates correctly."""
        self.assertEqual(self.checker.debt_ratio, 2.5)

    def test__check_cutoff(self) -> None:
        """Check that check_cutoff returns expected values."""
        self.assertEqual(
            self.checker._check_cutoff(type(self.checker)._loan_to_value_cutoffs, 0.4),
            0,
        )
        self.assertEqual(
            self.checker._check_cutoff(type(self.checker)._loan_to_value_cutoffs, 0.6),
            0.01,
        )
        self.assertEqual(
            self.checker._check_cutoff(type(self.checker)._loan_to_value_cutoffs, 0.8),
            0.02,
        )
        self.assertEqual(
            self.checker._check_cutoff(type(self.checker)._debt_ratio_cutoffs, 1), 0
        )
        self.assertEqual(
            self.checker._check_cutoff(type(self.checker)._debt_ratio_cutoffs, 5), 0.01
        )

    def test__convert_date_to_int(self) -> None:
        """Check that _convert_date_to_int returns expected value."""
        self.assertEqual(
            type(self.checker)._convert_date_to_int(date.fromisoformat("1998-03-05")),
            305,
        )

    def test_minimum_monthly_payment(self) -> None:
        """Check that minimum_monthly_payment returns expected values."""
        self.assertEqual(self.checker.minimum_monthly_payment, 0)
        self.checker.household_gross_income = 10
        self.assertEqual(self.checker.minimum_monthly_payment, 5e6 * 0.01 / 12)
        self.checker.household_gross_income = 2e6
        self.checker.principal = 6e6
        self.assertEqual(self.checker.minimum_monthly_payment, 5e6 * 0.01 / 12)
        self.checker.principal = 8e6
        self.assertEqual(self.checker.minimum_monthly_payment, 5e6 * 0.02 / 12)

    def test_set_birth_date(self) -> None:
        """Check that incorrect values raise error when setting birth date."""
        with self.assertRaises(ValueError):
            self.checker.birth_date = "not a date"

    def test_current_date(self) -> None:
        """Check that current date is set correctly."""
        self.assertEqual(self.checker.current_date.year, datetime.now().year)
        self.assertEqual(self.checker.current_date.month, datetime.now().month)
        self.assertEqual(self.checker.current_date.day, datetime.now().day)

    def test__first_date(self) -> None:
        """Check that _first_date returns expected value."""
        self.assertEqual(
            type(self.checker)._first_date(
                date.fromisoformat("1998-03-01"), date.fromisoformat("1986-07-08")
            ),
            0,
        )

    def test_age_has_had_birthday(self) -> None:
        """Tests whether age returns correct value after birthday."""
        self.checker._current_date = date.fromisoformat("2007-09-03")
        self.assertEqual(self.checker.age, 1)

    def test_age_has_not_had_birthday(self) -> None:
        """Tests whether age returns correct value before birthday."""
        self.checker._current_date = date.fromisoformat("2024-09-01")
        self.assertEqual(self.checker.age, 17)

    def test_risk_cost(self) -> None:
        """Check that risk cost calculations are correct."""
        self.checker.fund_value = 0.5e6
        for (
            age,
            cost_per_million,
        ) in self.checker._risk_cost_per_million_by_age_cutoffs.items():
            self.checker._birth_date = date(
                year=self.checker.current_date.year - age, month=1, day=1
            )
            self.assertEqual(self.checker.risk_cost, cost_per_million / 2)

    def test_rounded_age(self) -> None:
        """Check that rounded_age rounds to the closest 5 between 20 and 90."""
        ages_to_round = {2: 20, 150: 90}
        ages_to_round.update(
            {
                i[0]: i[1]
                for i in zip(
                    [i for i in range(19, 90, 5)], [i for i in range(20, 90, 5)]
                )
            }
        )
        ages_to_round.update(
            {
                i[0]: i[1]
                for i in zip(
                    [i for i in range(21, 90, 5)], [i for i in range(20, 90, 5)]
                )
            }
        )
        ages_to_round.update(
            {
                i[0]: i[1]
                for i in zip(
                    [i for i in range(17, 90, 5)], [i for i in range(20, 90, 5)]
                )
            }
        )
        ages_to_round.update(
            {
                i[0]: i[1]
                for i in zip(
                    [i for i in range(22, 90, 5)], [i for i in range(20, 90, 5)]
                )
            }
        )
        for actual_age, rounded_age in ages_to_round.items():
            self.checker._birth_date = date(
                year=self.checker.current_date.year - actual_age, month=1, day=1
            )
            self.assertEqual(self.checker.rounded_age, rounded_age)

    def test__is_leap_year(self) -> None:
        """Test that leap years are correctly identified."""
        self.assertFalse(self.checker._is_leap_year(2023))
        self.assertTrue(self.checker._is_leap_year(2024))

    def test__calculate_daily_interest_rate(self) -> None:
        """Test that daily interest rate calculates correctly."""
        initial_sum = 100
        yearly_percentage = 0.3
        leap_year = 2024
        non_leap_year = 2023
        daily_leap_year_rate = self.checker._calculate_daily_interest_rate(
            yearly_percentage, leap_year
        )
        daily_non_leap_year_rate = self.checker._calculate_daily_interest_rate(
            yearly_percentage, non_leap_year
        )

        self.assertAlmostEqual(
            initial_sum * daily_leap_year_rate**366,
            initial_sum * (1 + yearly_percentage),
        )
        self.assertAlmostEqual(
            initial_sum * daily_non_leap_year_rate**365,
            initial_sum * (1 + yearly_percentage),
        )

    def test_add_master_row(self):
        """Test all columns of add_master_row."""
        i = 0
        while i < 400:
            self.checker.add_master_row()
            i += 1

        # Check that date increases.
        self.assertEqual(
            self.checker.master_table.loc[1, "date"],
            pd.Timestamp("1994-06-02 00:00:00"),
        )

        # Check that principal increases.
        self.assertEqual(
            self.checker.master_table.loc[1, "principal"],
            np.float64(5001048.027231348),
        )

        # Check that current_month_interest resets avery month.
        self.assertFalse(
            any(
                self.checker.master_table.query("date.dt.day == 1")[
                    "current_month_interest"
                ]
            )
        )

        # Check that loan payment is calculated correctly.
        self.assertEqual(
            self.checker.master_table[
                self.checker.master_table["date"].dt.is_month_end
            ]["loan_payment"].iloc[0],
            np.float64(42924.68525463715),
        )

        # Check that fund investment is calculated correctly.
        self.assertEqual(
            self.checker.master_table[
                self.checker.master_table["date"].dt.is_month_end
            ]["fund_investment"].iloc[0],
            np.float64(8333.333333333334),
        )

        # Check that loan payment affects principal column.
        self.assertGreater(
            self.checker.master_table["principal"].iloc[28],
            self.checker.master_table["principal"].iloc[27],
        )
        self.assertLess(
            self.checker.master_table["principal"].iloc[29],
            self.checker.master_table["principal"].iloc[28],
        )

        # Check that fund investment affects index fund value column.
        self.assertGreater(
            self.checker.master_table["fund_value"].iloc[29],
            self.checker.master_table["fund_value"].iloc[28],
        )

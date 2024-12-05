import numpy as np
import pandas as pd

from datetime import datetime, date

from src.loan.historic_tables import HistoricTables


class Mortgage:
    """Analyze costs of a Swedish house loan.

    A class for storing data about and calculating costs associated with
    getting a mortgage in Sweden and paying it off over time as compared
    with investing the same amount in an index fund and then paying off the
    loan as a lump sum instead.

    Attributes:
        asset_value: Value of the asset mortgaged.
        household_gross_income: Household income before tax.
        index_fund_value: Value of index fund.
        initial_principal: Original amount borrowed.
        principal: Amount borrowed.
        omxs30_change_multiplier: Daily OMXS30 change multiplier.
        bank_rate: Daily bank rate multiplier.
        standard_rate: Yearly standard rate for calculating capital tax.
        historic_date_range: Dates from where historic data is taken.
        payoff_time: Planned years to pay off entire principal.
        days_offset: Initial offset to use in historic data.
        fraction_invested: Proportion of residual monthly payment invested.
    """

    # The following dictionaries contain cutoff values for minmum yearly
    # percentages of the principal to be paid, according to Finansinspektionen.
    # The keys represent the cutoff value and the values represent the minimum
    # percentage. E.g. a _loan_to_value_cuttoffs of {0.7: 0.02, 0.5: 0.1.}
    # means that 2% yearly has to be paid if the loan-to-value ratio is over
    # 70% and 1% yearly if it is over 50%.
    _loan_to_value_cutoffs = {0.7: 0.02, 0.5: 0.01}
    _debt_ratio_cutoffs = {4.5: 0.01}
    _risk_cost_per_million_by_age_cutoffs = {
        20: 0.7,
        25: 0.72,
        30: 0.56,
        35: 0.72,
        40: 1.05,
        45: 1.73,
        50: 2.94,
        55: 4.66,
        60: 7.42,
        65: 13.30,
        70: 21.1,
        75: 35.56,
        80: 63.94,
        85: 114.4,
        90: 196.42,
    }

    _default_historic_tables = HistoricTables()

    @classmethod
    def _check_cutoff(cls, cutoff_dict: dict, cutoff_value: float) -> float:
        """Return max dict value where cutoff_value is larger than dict key.

        Args:
            cutoff_dict: A dict formatted as cutoff values to check: values to
            return.
            cutoff_value: The cutoff value to check agains the cutoff dict.

        Returns:
            The dict value corresponding to cutoff_value.
        """
        return max(
            [value if cutoff_value > key else 0 for key, value in cutoff_dict.items()]
        )

    @classmethod
    def _convert_date_to_int(cls, date_to_convert: date) -> int:
        """Converts a date to an integer, formatted as MMDD.

        Args:
            date_to_convert: A datetime object.

        Returns:
            An integer, formatted as MMDD.
        """
        return int(date_to_convert.strftime("%m%d"))

    @classmethod
    def _first_date(cls, date_one: date, date_two: date) -> int:
        """Check which date comes first in the year, disregarding the year.

        Args:
            date_one: A datetime object.
            date_two: A datetime object.

        Returns:
            The index of the first date in the year. I.e. 0 for date_one or 1
            for date_two.
        """
        date_list = [
            cls._convert_date_to_int(date_one),
            cls._convert_date_to_int(date_two),
        ]
        first_date_index = date_list.index(min(date_list))
        return first_date_index

    @classmethod
    def _calculate_daily_interest_rate(
        cls, yearly_interest_rate: float, year: int
    ) -> float:
        """Convert yearly interest to daily interest.

        Convert a yearly interest to a daily interest. In reality a - 1 should
        be added at the end to calculate rate of change but this was omitted to
        simplify further calculations usning the rate.

        Args:
            yearly_interest_rate: The yearly interest.
            year: The calendar year.

        Return:
            A float.
        """
        daily_interest_rate = (1 + yearly_interest_rate) ** (
            1 / (365 + cls._is_leap_year(year))
        )
        return daily_interest_rate

    @classmethod
    def _is_leap_year(cls, year: int) -> bool:
        """Return True if leap year.

        Returns:
            A boolean.
        """
        try:
            _ = date(year=year, month=2, day=29)
            return True
        except ValueError:
            return False

    def __init__(
        self,
        asset_value: float,
        birth_date: str,
        household_gross_income: float,
        principal: float,
        payoff_time: float,
        interest_markup: float,
        days_offset: int = 0,
        fraction_invested: int = 1,
        historic_tables=_default_historic_tables,
    ) -> None:
        """Initialize Mortgage instance.

        Args:
            asset_value: Value of the asset mortgaged.
            birth_date: Birth date of index fund owner.
            household_gross_income: Household income before tax.
            principal: Amount borrowed.
            payoff_time: Number of years to pay off loan.
            interest_markup: The markup on the policy rate, used by the bank.
            days_offset: Initial offset to use in historic data.
            historic_tables: A HistoricTables object.
            fraction_invested: Proportion of residual monthly payment invested.
        """
        self.asset_value = asset_value
        self.birth_date = birth_date
        self._current_date = datetime.now()
        self.household_gross_income = household_gross_income
        self.index_fund_value = 0
        self.initial_principal = principal
        self.principal = principal
        self.omxs30_change_multiplier = np.array(
            historic_tables.main_table.omxs30_change_multiplier
        )
        self.bank_rate = np.array(
            historic_tables.main_table.apply(
                lambda x: self._calculate_daily_interest_rate(
                    x["policy_rate"] + interest_markup, x["date"].year
                ),
                axis=1,
            )
        )
        self.standard_rate = np.array(historic_tables.main_table.standard_rate)
        self.historic_date_range = np.array(historic_tables.main_table.date)
        self.days_offset = days_offset
        self.payoff_time = payoff_time
        self.fraction_invested = fraction_invested
        self._master_table = pd.DataFrame(
            {
                "date": [self.historic_date_range[days_offset]],
                "principal": [self.principal],
                "current_month_interest": [0],
                "loan_payment": [0],
                "fund_investment": [0],
            }
        )

    @property
    def birth_date(self) -> date:
        """Return birth date."""
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: str) -> None:
        """Set birth date from an ISO format string."""
        self._birth_date = date.fromisoformat(value)

    @property
    def current_date(self) -> date:
        """Current date, incremented for future calculations."""
        return self._current_date

    @property
    def loan_to_value_ratio(self) -> float:
        """Ratio of principal to asset value."""
        return self.principal / self.asset_value

    @property
    def debt_ratio(self) -> float:
        """Ratio of principal to household gross income."""
        return self.principal / self.household_gross_income

    @property
    def minimum_monthly_payment(self) -> float:
        """Return the minimum legal monthly payment amount."""
        yearly_minimum_percentage = max(
            type(self)._check_cutoff(
                type(self)._loan_to_value_cutoffs, self.loan_to_value_ratio
            ),
            type(self)._check_cutoff(type(self)._debt_ratio_cutoffs, self.debt_ratio),
        )
        minimum_monthly_payment = (
            self.initial_principal * yearly_minimum_percentage / 12
        )
        return minimum_monthly_payment

    @property
    def age(self) -> int:
        """Return age of index fund owner."""
        year_delta = self.current_date.year - self.birth_date.year
        has_not_had_birthday = type(self)._first_date(
            self.birth_date, self.current_date
        )
        return year_delta - has_not_had_birthday

    @property
    def rounded_age(self) -> int:
        """Age rounded to closest five between 20 and 150."""
        match self.age:
            case self.age if self.age < 20:
                return 20
            case self.age if self.age > 90:
                return 90
            case _:
                return 5 * round(self.age / 5)

    @property
    def risk_cost(self) -> float:
        risk_cost_per_million = self._risk_cost_per_million_by_age_cutoffs[
            self.rounded_age
        ]
        return self.index_fund_value * risk_cost_per_million / 1e6

    @property
    def master_table(self) -> pd.DataFrame:
        """Return master table."""
        return self._master_table

    @property
    def total_monthly_payment(self):
        """Return required monthly payment to make payoff time."""
        return self.initial_principal / (self.payoff_time * 12)

    @property
    def payment_split(self):
        """Return split between loan payment and fund investment."""
        fund_investment = self.total_monthly_payment * self.fraction_invested
        loan_payment = (
            self.total_monthly_payment - fund_investment + self.minimum_monthly_payment
        )
        return {"loan_payment": loan_payment, "fund_investment": fund_investment}

    def add_master_row(self) -> None:
        """Add row to master table."""
        idx = len(self.master_table) + self.days_offset

        # Set date corresponding to index and initial offset.
        new_date = self.historic_date_range[idx]

        # Multiply previous principal with daily interest rate.
        self.principal = (
            self.master_table["principal"].iloc[-1] * self.bank_rate[idx - 1]
        )

        # Calculate change of principal during the current month, which
        # corresponds to the accumulated interest during the month.
        first_day_of_month = pd.Timestamp(new_date).replace(day=1)
        first_day_of_month_principal = self.master_table.query(
            "date == @first_day_of_month"
        )

        if first_day_of_month_principal.empty:
            new_current_month_interest = 0
        else:
            new_current_month_interest = (
                self.principal
                - first_day_of_month_principal.reset_index().loc[0, "principal"]
            )

        # Calculate loan payment and fund investment.
        payments = self.payment_split
        payments["loan_payment"] += new_current_month_interest
        if not pd.Timestamp(new_date).is_month_end:
            for key in payments.keys():
                payments[key] = 0
        loan_payment = payments["loan_payment"]
        fund_investment = payments["fund_investment"]

        new_row = pd.DataFrame(
            {
                "date": [new_date],
                "principal": [self.principal],
                "current_month_interest": [new_current_month_interest],
                "loan_payment": [loan_payment],
                "fund_investment": [fund_investment],
            }
        )

        self._master_table = pd.concat([self._master_table, new_row]).reset_index(
            drop=True
        )

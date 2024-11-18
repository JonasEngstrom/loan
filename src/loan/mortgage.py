class Mortgage:
    """Analyze costs of a Swedish house loan.

    A class for storing data about and calculating costs associated with
    getting a mortgage in Sweden and paying it off over time as compared
    with investing the same amount in an index fund and then paying off the
    loan as a lump sum instead.

    Attributes:
        asset_value: Value of the asset mortgaged.
        household_gross_income: Household income before tax.
        initial_principal: Original amount borrowed.
        principal: Amount borrowed.
    """

    # The following dictionaries contain cutoff values for minmum yearly
    # percentages of the principal to be paid, according to Finansinspektionen.
    # The keys represent the cutoff value and the values represent the minimum
    # percentage. E.g. a _loan_to_value_cuttoffs of {0.7: 0.02, 0.5: 0.1.}
    # means that 2% yearly has to be paid if the loan-to-value ratio is over
    # 70% and 1% yearly if it is over 50%.
    _loan_to_value_cutoffs = {0.7: 0.02, 0.5: 0.01}
    _debt_ratio_cutoffs = {4.5: 0.01}

    @classmethod
    def _check_cutoff(cls, cutoff_dict: dict, cutoff_value: float) -> float:
        """Return max dict value where cutoff_value is larger than dict key."""
        return max(
            [value if cutoff_value > key else 0 for key, value in cutoff_dict.items()]
        )

    def __init__(
        self, asset_value: float, household_gross_income: float, principal: float
    ) -> None:
        """Initialize Mortgage instance.

        Args:
            asset_value: Value of the asset mortgaged.
            household_gross_income: Household income before tax.
            principal: Amount borrowed.
        """
        self.asset_value = asset_value
        self.household_gross_income = household_gross_income
        self.initial_principal = principal
        self.principal = principal

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

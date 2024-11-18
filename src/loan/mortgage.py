class Mortgage:
    """Analyze costs of a Swedish house loan.

    A class for storing data about and calculating costs associated with
    getting a mortgage in Sweden and paying it off over time as compared
    with investing the same amount in an index fund and then paying off the
    loan as a lump sum instead.

    Attributes:
        asset_value: Value of the asset mortgaged.
        initial_principal: Original amount borrowed.
        principal: Amount borrowed.
    """

    def __init__(self, asset_value: float, principal: float) -> None:
        """Initialize Mortgage instance.

        Args:
            asset_value: Value of the asset mortgaged.
            principal: Amount borrowed.
        """
        self.asset_value = asset_value
        self.initial_principal = principal
        self.principal = principal

    @property
    def loan_to_value_ratio(self) -> float:
        """Loan-to-value ratio."""
        return self.principal / self.asset_value

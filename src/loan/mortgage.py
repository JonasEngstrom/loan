class Mortgage:
    """Analyze costs of a Swedish house loan.

    A class for storing data about and calculating costs associated with
    getting a mortgage in Sweden and paying it off over time as compared
    with investing the same amount in an index fund and then paying off the
    loan as a lump sum instead.

    Attributes:
        initial_principal: The original amount borrowed.
    """

    def __init__(self, initial_principal: float) -> None:
        """Initialize Mortgage instance.

        Args:
            inital_principal: Initial amount borrowed.
        """
        self.initial_principal = initial_principal

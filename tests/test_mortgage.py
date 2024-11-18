import unittest

from src.loan import mortgage


class TestMortgage(unittest.TestCase):
    """Test case for Mortgage class."""

    def __init__(self, method_name: str = "runTest") -> None:
        """Set up test case for Mortgage class."""
        super().__init__(method_name)
        self.checker = mortgage.Mortgage(
            asset_value=10e6, household_gross_income=2e6, principal=5e6
        )

    def test__init__(self) -> None:
        """Check that __init__ exhibits expected behavior."""
        self.assertEqual(self.checker.asset_value, 10e6)
        self.assertEqual(self.checker.household_gross_income, 2e6)
        self.assertEqual(self.checker.initial_principal, 5e6)
        self.assertEqual(self.checker.principal, 5e6)

    def test_loan_to_value_ratio(self) -> None:
        """Check that loan-to-value ratio calculates correctly."""
        self.assertEqual(self.checker.loan_to_value_ratio, 0.5)

    def test_debt_ratio(self) -> None:
        """Check that debt ratio calculates correctly."""
        self.assertEqual(self.checker.debt_ratio, 2.5)

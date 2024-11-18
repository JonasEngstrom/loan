import unittest

from src.loan import mortgage


class TestMortgage(unittest.TestCase):
    """Test case for Mortgage class."""

    def __init__(self, method_name: str = "runTest") -> None:
        """Set up test case for Mortgage class."""
        super().__init__(method_name)
        self.checker = mortgage.Mortgage(initial_principal=5e6)

    def test__init__(self):
        """Check that __init__ exhibits expected behavior."""
        self.assertEqual(self.checker.initial_principal, 5e6)

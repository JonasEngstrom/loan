import unittest

from src.loan import local_data

import numpy as np


class TestLocalData(unittest.TestCase):
    """Test the functions in local_data.py."""

    def __init__(self, method_name: str = "runTest") -> None:
        """Initialize test class."""
        super().__init__(method_name)

    def test_old_omxs30_data(self):
        """Test that old_omxs30_data.csv loads as expected."""
        test_data = local_data.old_omxs30_data()
        self.assertEqual(test_data.iloc[0, 1], np.float64(2626.57))

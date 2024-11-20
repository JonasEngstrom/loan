import unittest
from unittest.mock import patch

from src.loan import download

import numpy as np


class MockResponse:
    """Mock requests.get responses."""

    def __init__(self, text, status_code):
        self.text = text
        self.status_code = status_code


def mocked_request_get_404(*args, **kwargs):
    """Mock 404 status code."""
    return MockResponse("foo", 404)


def mocked_requests_get_200_gbr(*args, **kwargs):
    """Mock government borrowing rate CSV."""
    text = "Datum;Räntesats %;Medelvärde hittills i år\r\n2024-11-15;2,11;2,16\r\n2024-11-08;2,10;2,16\r\n2024-11-01;2,02;2,16\r\n"
    return MockResponse(text, 200)


class TestDownload(unittest.TestCase):
    """Tests the functions in download.py."""

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    @patch("requests.get", side_effect=mocked_request_get_404)
    def test_government_borrowing_rate_status_code_not_200(self, mock_get) -> None:
        """Assert government_borrowing_rate raises error if status not 200."""
        with self.assertRaises(ConnectionError):
            download.government_borrowing_rate()

    @patch("requests.get", side_effect=mocked_requests_get_200_gbr)
    def test_government_borrowing_rate_status_code_200(self, mock_get) -> None:
        """Assert government_borrowing_rate imports data correctly."""
        test_df = download.government_borrowing_rate()
        self.assertEqual(
            list(
                test_df.columns.values,
            ),
            ["Datum", "Räntesats %", "Medelvärde hittills i år"],
        )
        self.assertEqual(test_df.iloc[2, 2], np.float64(2.16))
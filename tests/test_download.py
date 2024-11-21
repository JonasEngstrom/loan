import unittest
from unittest.mock import patch

from src.loan import download

import numpy as np
import json


class MockResponse:
    """Mock requests.get/post responses.

    Attributes:
        text: Text and JSON value returned.
        status_code: Request status code returned.
    """

    def __init__(self, text, status_code):
        """Set text (and thereby json) and status code.

        Args:
            test: Text and JSON value to return.
            status_code: Request status code to return.
        """
        self.text = text
        self.status_code = status_code

    def json(self):
        """Return text attribute as json, for testing."""
        return json.loads(self.text)


def mocked_request_404(*args, **kwargs):
    """Mock 404 status code."""
    return MockResponse("foo", 404)


def mocked_requests_get_200_gbr(*args, **kwargs):
    """Mock government borrowing rate CSV."""
    text = "Datum;Räntesats %;Medelvärde hittills i år\r\n2024-11-15;2,11;2,16\r\n2024-11-08;2,10;2,16\r\n2024-11-01;2,02;2,16\r\n"
    return MockResponse(text, 200)


def mocked_requests_post_200_cpi(*args, **kwargs):
    """Mock consumer price index CSV."""
    text = '"Tid","ContentsCode","TAB5737"\r\n"1980M01","000004VU",95.30\r\n"1980M02","000004VU",96.80\r\n"1980M03","000004VU",97.20\r\n'
    return MockResponse(text, 200)


def mocked_requests_get_200_pr(*args, **kwargs):
    """Mock policy rate CSV."""
    text = '[{"date":"1994-06-01","value":6.95},{"date":"1994-06-02","value":6.95},{"date":"1994-06-03","value":6.95}]'
    return MockResponse(text, 200)


def mocked_requests_get_200_omxs30(*args, **kwargs):
    """Mock OMXS30 CSV."""
    text = '{"data":{"chartData":{"orderbookId":"SE0000337842","assetClass":"INDEXES","isin":"SE0000337842","symbol":"OMXS30","company":"OMX Stockholm 30 Index","timeAsOf":"2024-11-20","lastSalePrice":"2,484.49","netChange":"-8.99","percentageChange":"-0.36%","deltaIndicator":"up","previousClose":"2,493.47"},"charts":{"headers":{"dateTime":"Date","high":"High price","low":"Low price","close":"Closing price","average":"Average price","totalVolume":"Total volume","turnover":"Turnover"},"rows":[{"dateTime":"2024-11-20","bid":"","ask":"","open":"2,508.29","high":"2,513.74","low":"2,483.49","close":"2,484.49","average":"","totalVolume":"1","turnover":"","trades":""},{"dateTime":"2024-11-19","bid":"","ask":"","open":"2,515.21","high":"2,518.15","low":"2,462.17","close":"2,493.48","average":"","totalVolume":"1","turnover":"","trades":""},{"dateTime":"2024-11-18","bid":"","ask":"","open":"2,509.39","high":"2,518.88","low":"2,489.89","close":"2,506.91","average":"","totalVolume":"1","turnover":"","trades":""},{"dateTime":"2024-11-15","bid":"","ask":"","open":"2,513.49","high":"2,530.64","low":"2,506.38","close":"2,509.99","average":"","totalVolume":"1","turnover":"","trades":""}]}},"messages":null,"status":{"timestamp":"2024-11-21T02:02:23+0100","rCode":200,"bCodeMessage":null,"developerMessage":""}}'
    return MockResponse(text, 200)


class TestDownload(unittest.TestCase):
    """Tests the functions in download.py."""

    def __init__(self, method_name: str = "runTest") -> None:
        super().__init__(method_name)

    @patch("requests.get", side_effect=mocked_request_404)
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

    @patch("requests.post", side_effect=mocked_request_404)
    def test_consumer_price_index_status_code_not_200(self, mock_post) -> None:
        """Assert consumer_price_index raises error if status not 200."""
        with self.assertRaises(ConnectionError):
            download.consumer_price_index()

    @patch("requests.post", side_effect=mocked_requests_post_200_cpi)
    def test_consumer_price_index_status_code_200(self, mock_post) -> None:
        """Assert consumer_price_index imports data correctly."""
        test_df = download.consumer_price_index()
        self.assertEqual(
            list(
                test_df.columns.values,
            ),
            ["date", "consumer_price_index"],
        )
        self.assertEqual(test_df.iloc[1, 1], np.float64(96.8))

    @patch("requests.get", side_effect=mocked_request_404)
    def test_policy_rate_status_code_not_200(self, mock_get) -> None:
        """Assert consumer_price_index raises error if status not 200."""
        with self.assertRaises(ConnectionError):
            download.policy_rate()

    @patch("requests.get", side_effect=mocked_requests_get_200_pr)
    def test_policy_rate_status_code_200(self, mock_get) -> None:
        """Assert policy_rate imports data correctly."""
        test_df = download.policy_rate()
        self.assertEqual(
            list(
                test_df.columns.values,
            ),
            ["date", "policy_rate"],
        )
        self.assertEqual(test_df.iloc[2, 1], np.float64(6.95))

    @patch("requests.get", side_effect=mocked_request_404)
    def test_omxs30_status_code_not_200(self, mock_get) -> None:
        """Assert omxs30x raises error if status not 200."""
        with self.assertRaises(ConnectionError):
            download.omxs30()

    @patch("requests.get", side_effect=mocked_requests_get_200_omxs30)
    def test_omxs30_status_code_200(self, mock_get) -> None:
        """Assert omxs30 imports data correctly."""
        test_df = download.omxs30()
        self.assertEqual(
            list(
                test_df.columns.values,
            ),
            [
                "date",
                "bid",
                "ask",
                "open",
                "high",
                "low",
                "close",
                "average",
                "total_volume",
                "turnover",
                "trades",
            ],
        )
        self.assertEqual(test_df.iloc[1, 3], np.float64(2515.21))

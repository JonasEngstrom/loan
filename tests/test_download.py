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


def mocked_requests_get_200_list_rates(*args, **kwargs):
    """Mock OMXS30 CSV."""
    text = '[{"CategoryName": "Aktuella listr\u00e4ntor - annonserade r\u00e4ntor","CategorySubHeader": null,"CategoryDescription": "R\u00e4ntorna \u00e4r senast uppdaterade 2024-11-15","Headers": [{"Id": 0,"Name": "F\u00f6retag","Description": null,"ComparisonCategoryId": 0},{"Id": 10280,"Name": "R\u00f6rlig","Description": null,"ComparisonCategoryId": 2535},{"Id": 10226,"Name": "3 m\u00e5n","Description": null,"ComparisonCategoryId": 2535},{"Id": 10227,"Name": "1 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10228,"Name": "2 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10229,"Name": "3 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10230,"Name": "4 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10231,"Name": "5 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10232,"Name": "6 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10233,"Name": "7 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10234,"Name": "8 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10235,"Name": "9 \u00e5r","Description": null,"ComparisonCategoryId": 2535},{"Id": 10236,"Name": "10 \u00e5r","Description": null,"ComparisonCategoryId": 2535}],"CompensationRows": [{"CompensationItems": [{"CompensationValue": "Avanza Bank","Description": null,"Date": "2022-11-07","Url": "http://www.avanza.se","ProductName": "Superbol\u00e5net","HideDate": true,"ComparisonCategoryId": 0,"HeaderId": 0},{"CompensationValue": "3,01 - 3,35","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10280},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10226},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10227},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10228},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10229},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10230},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10231},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10232},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10233},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10234},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10235},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10236}]},{"CompensationItems": [{"CompensationValue": "Bluestep","Description": null,"Date": "2022-11-07","Url": "http://www.bluestep.se/","ProductName": "","HideDate": true,"ComparisonCategoryId": 0,"HeaderId": 0},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10280},{"CompensationValue": "5,90 - 10,95","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10226},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10227},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10228},{"CompensationValue": "5,70 - 10,95","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10229},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10230},{"CompensationValue": "6,05 - 10,95","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10231},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10232},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10233},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10234},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10235},{"CompensationValue": "","Description": null,"Date": null,"Url": null,"ProductName": null,"HideDate": false,"ComparisonCategoryId": 2535,"HeaderId": 10236}]}],"CategoryId": 2535,"AnchorLink": "aktuella-listrantor---annonserade-rantor"}]'
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
            ["date", "government_borrowing_rate", "current_year_average"],
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

    @patch("requests.get", side_effect=mocked_request_404)
    def test_list_rates_status_code_not_200(self, mock_get) -> None:
        """Assert list_rates raises error if status not 200."""
        with self.assertRaises(ConnectionError):
            download.list_rates()

    @patch("requests.get", side_effect=mocked_requests_get_200_list_rates)
    def test_list_rates_status_code_200(self, mock_get) -> None:
        """Assert list_rates imports data correctly."""
        test_df = download.list_rates()
        self.assertEqual(
            list(
                test_df.columns.values,
            ),
            [
                "bank",
                "floating",
                "three_months",
                "one_year",
                "two_years",
                "three_years",
                "four_years",
                "five_years",
                "six_years",
                "seven_years",
                "eight_years",
                "nine_years",
                "ten_years",
                "date",
            ],
        )
        self.assertEqual(test_df.iloc[0, 1], np.float64(3.01))
        self.assertEqual(test_df.iloc[1, 2], np.float64(5.9))

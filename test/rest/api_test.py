import http.client
import os
import unittest
from unittest.mock import patch
from urllib.request import urlopen
from urllib.error import HTTPError  # <- clave

import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


def mocked_validation(*args, **kwargs):
    return True


def _read_number(resp) -> float:
    """Lee el cuerpo (bytes), decodifica, hace strip y lo convierte a float."""
    return float(resp.read().decode().strip())


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/2/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertAlmostEqual(4.0, _read_number(response), places=6, msg="Resultado incorrecto")

    def test_api_substract(self):
        url = f"{BASE_URL}/calc/substract/5/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK)
        self.assertAlmostEqual(2.0, _read_number(response), places=6)

    @patch("app.util.validate_permissions", side_effect=mocked_validation, create=True)
    def test_api_multiply(self, _validate_permissions):
        url = f"{BASE_URL}/calc/multiply/3/4"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK)
        self.assertAlmostEqual(12.0, _read_number(response), places=6)

    def test_api_divide(self):
        url = f"{BASE_URL}/calc/divide/10/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK)
        self.assertAlmostEqual(5.0, _read_number(response), places=6)

    def test_api_divide_by_zero(self):
        url = f"{BASE_URL}/calc/divide/10/0"
        with self.assertRaises(HTTPError) as cm:
            urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(cm.exception.code, http.client.BAD_REQUEST)

    def test_api_power(self):
        url = f"{BASE_URL}/calc/power/2/3"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK)
        self.assertAlmostEqual(8.0, _read_number(response), places=6)

    def test_api_sqrt(self):
        url = f"{BASE_URL}/calc/sqrt/16"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK)
        self.assertAlmostEqual(4.0, _read_number(response), places=6)

    def test_api_log10(self):
        url = f"{BASE_URL}/calc/log10/100"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(response.status, http.client.OK)
        self.assertAlmostEqual(2.0, _read_number(response), places=6)

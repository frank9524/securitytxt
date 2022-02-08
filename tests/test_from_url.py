import os
import unittest
import operator
import requests_mock

from securitytxt.securitytxt import SecurityTXT


@requests_mock.Mocker()
class TestFromURL(unittest.TestCase):
    example_file = open(f"{os.path.dirname(os.path.realpath(__file__))}/files/test_signed/in.txt").read()
    expected_result = open(f"{os.path.dirname(os.path.realpath(__file__))}/files/test_signed/out.txt").read()

    def test_existing_securitytxt_standard_location(self, m: requests_mock.Mocker):
        url = "https://test.com/.well-known/security.txt"
        m.get(url, text=self.example_file, status_code=200)
        result = self.get_result(url)
        self.assertEqual(result, self.expected_result)

    def test_existing_securitytxt_no_protocol(self, m: requests_mock.Mocker):
        m.get("https://test.com/.well-known/security.txt", text=self.example_file, status_code=200)
        result = self.get_result("test.com")
        self.assertEqual(result, self.expected_result)

    def test_existing_root_securitytxt(self, m: requests_mock.Mocker):
        m.get(requests_mock.ANY, status_code=404)
        m.get("https://test.com/security.txt", text=self.example_file, status_code=200)
        result = self.get_result("test.com")
        self.assertEqual(result, self.expected_result)

    def test_http_securitytxt(self, m: requests_mock.Mocker):
        m.get(requests_mock.ANY, status_code=404)
        m.get("http://test.com/security.txt", text=self.example_file, status_code=200)
        result = self.get_result("test.com")
        self.assertEqual(result, self.expected_result)

    def test_existing_strict_url(self, m: requests_mock.Mocker):
        url = "https://test.com/random/security.txt"
        m.get(requests_mock.ANY, status_code=404)
        m.get(url, text=self.example_file, status_code=200)
        result = self.get_result(url, strict_url=True)
        self.assertEqual(result, self.expected_result)

    def test_nonexisting_strict_url(self, m: requests_mock.Mocker):
        with self.assertRaises(FileNotFoundError):
            m.get(requests_mock.ANY, status_code=404)
            m.get("https://test.com/random/security.txt", text=self.example_file, status_code=200)
            self.get_result("https://test.com/something_else/security.txt", strict_url=True)

    def test_nonexisting_securitytxt(self, m: requests_mock.Mocker):
        with self.assertRaises(FileNotFoundError):
            m.get(requests_mock.ANY, status_code=404)
            self.get_result("test.com", strict_url=True)

    def test_nonexisting_securitytxt_with_html_404(self, m: requests_mock.Mocker):
        with self.assertRaises(FileNotFoundError):
            m.get(requests_mock.ANY, status_code=200, text="<html><body>This page could not be found</body></html>")
            self.get_result("test.com")

    def test_prioritize_https(self, m: requests_mock.Mocker):
        m.get(requests_mock.ANY, status_code=404)
        m.get("https://test.com/.well-known/security.txt", text=self.example_file, status_code=200)
        m.get("http://test.com/.well-known/security.txt", text="Contact: test@test.com", status_code=200)
        result = self.get_result("test.com")
        self.assertEqual(result, self.expected_result)

    def get_result(self, url: str, strict_url=False) -> str:
        securitytxt = SecurityTXT.from_url(url, strict_url)
        result = {k: v for k, v in sorted(securitytxt.__dict__.items(), key=operator.itemgetter(0))}
        result['source_url'] = None
        return str(result)


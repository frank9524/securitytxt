import os
import unittest
import operator
import requests_mock

from securitytxt.securitytxt import SecurityTXT


@requests_mock.Mocker()
class TestFromURL(unittest.TestCase):
    files_dir = f"{os.path.dirname(os.path.realpath(__file__))}/files/"

    def test_existing_securitytxt_standard_location(self, m: requests_mock.Mocker):
        url = "https://test.com/.well-known/security.txt"
        m.get(url, text=open(f"{self.files_dir}/test_signed/in.txt").read(), status_code=200)
        result = self.get_result(url)
        expected_result = open(f"{self.files_dir}/test_signed/out.txt").read()
        self.assertEqual(result, expected_result)

    def test_existing_securitytxt_no_protocol(self, m: requests_mock.Mocker):
        url = "https://test.com/.well-known/security.txt"
        m.get(url, text=open(f"{self.files_dir}/test_signed/in.txt").read(), status_code=200)
        result = self.get_result("test.com")
        expected_result = open(f"{self.files_dir}/test_signed/out.txt").read()
        self.assertEqual(result, expected_result)

    def test_existing_root_securitytxt(self, m: requests_mock.Mocker):
        url = "https://test.com/security.txt"
        m.get(requests_mock.ANY, status_code=404)
        m.get(url, text=open(f"{self.files_dir}/test_signed/in.txt").read(), status_code=200)
        result = self.get_result("test.com")
        expected_result = open(f"{self.files_dir}/test_signed/out.txt").read()
        self.assertEqual(result, expected_result)

    def test_http_securitytxt(self, m: requests_mock.Mocker):
        url = "http://test.com/security.txt"
        m.get(requests_mock.ANY, status_code=404)
        m.get(url, text=open(f"{self.files_dir}/test_signed/in.txt").read(), status_code=200)
        result = self.get_result("test.com")
        expected_result = open(f"{self.files_dir}/test_signed/out.txt").read()
        self.assertEqual(result, expected_result)

    def test_existing_strict_url(self, m: requests_mock.Mocker):
        url = "https://test.com/random/security.txt"
        m.get(requests_mock.ANY, status_code=404)
        m.get(url, text=open(f"{self.files_dir}/test_signed/in.txt").read(), status_code=200)
        result = self.get_result(url, strict_url=True)
        expected_result = open(f"{self.files_dir}/test_signed/out.txt").read()
        self.assertEqual(result, expected_result)

    def test_nonexisting_strict_url(self, m: requests_mock.Mocker):
        with self.assertRaises(FileNotFoundError):
            url = "https://test.com/random/security.txt"
            m.get(requests_mock.ANY, status_code=404)
            m.get(url, text=open(f"{self.files_dir}/test_signed/in.txt").read(), status_code=200)
            self.get_result("https://test.com/something_else/security.txt", strict_url=True)

    def test_nonexisting_securitytxt(self, m: requests_mock.Mocker):
        with self.assertRaises(FileNotFoundError):
            m.get(requests_mock.ANY, status_code=404)
            self.get_result("test.com", strict_url=True)

    def test_nonexisting_securitytxt_with_html_404(self, m: requests_mock.Mocker):
        with self.assertRaises(FileNotFoundError):
            m.get(requests_mock.ANY, status_code=200, text="<html><body>This page could not be found</body></html>")
            self.get_result("test.com")

    def get_result(self, url: str, strict_url=False) -> str:
        securitytxt = SecurityTXT.from_url(url, strict_url)
        result = {k: v for k, v in sorted(securitytxt.__dict__.items(), key=operator.itemgetter(0))}
        result['source_url'] = None
        return str(result)


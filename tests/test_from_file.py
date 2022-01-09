import operator
import unittest
import os

from securitytxt.securitytxt import SecurityTXT


class TestFromFile(unittest.TestCase):

    def test_from_file(self):
        files_dir = f"{os.path.dirname(os.path.realpath(__file__))}/files/"
        folders = next(os.walk(files_dir))[1]
        for folder in folders:
            with self.subTest(msg=f"Checking test case {folder}"):
                dir = f"{files_dir}/{folder}"
                result = self.get_result(dir)
                expected_result = self.get_expected_result(dir)
                self.assertEqual(result, expected_result)

    def get_result(self, dir: str) -> str:
        with open(f"{dir}/in.txt", 'r') as in_file:
            securitytxt = SecurityTXT.from_text(in_file.read())
        result = {k: v for k, v in sorted(securitytxt.__dict__.items(), key=operator.itemgetter(0))}
        return str(result)

    def get_expected_result(self, dir: str) -> str:
        with open(f"{dir}/out.txt", 'r') as out_file:
            return out_file.read()



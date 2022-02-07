from typing import Optional, List, Dict

from urllib.parse import urlparse
from requests import get, exceptions

from securitytxt.parsers.file_parser import FileParser
from securitytxt.securitytxt import SecurityTXT


class URLParser:
    """Takes a URL, looks for security.txt files on the domain and when found, parses the security.txt file.
    Creating an object of the parser immediately parses the given url.

    Attributes:
        :class possible_paths: the paths where to look for a security.txt on a domain. Overridable in the __init__.
        :class headers: the headers for the request. Overridable in the __init__.
        :class default_scheme: the default scheme for requests, if no scheme is provided.
        securitytxt: the resulting securitytxt after parsing.
        strict_url: Whether to actively look for a securitytxt on the domain of the url, or whether to 'strictly' use
        the provided url. Default is False.

    Public methods:
        None

    Raises:
        :raises FileNotFoundError: if no security.txt could be found on the url.
    """
    possible_paths = ['/.well-known/security.txt', '/security.txt']
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
    possible_schemes = ["https", "http"]

    def __init__(self, url: str, strict_url: bool = False, possible_paths: Optional[List[str]] = None,
                 headers: Optional[Dict] = None, possible_schemes: Optional[List[str]] = None):
        """Initialize the variables."""
        self.securitytxt: Optional[SecurityTXT] = None
        self.strict_url = strict_url
        self.possible_paths = possible_paths if possible_paths else self.possible_paths
        self.headers = headers if headers else self.headers
        self.possible_schemes = possible_schemes if possible_schemes else self.possible_schemes
        self._parse(url)

    def _parse(self, url: str) -> None:
        """
        Look for security.txt files on the domain and parse if one is found.
        :param url: The url to search for a security.txt.
        :raises FileNotFoundError: if no security.txt could be found on the url.
        """
        possible_file_urls = self._get_possible_file_urls(url)
        # For all possible urls where a security.txt could be located, check if there is one.
        for file_url in possible_file_urls:
            if self._parse_file_url(file_url):
                # The file has been parsed and set, so we can stop looking for other security.txt files
                return
        raise FileNotFoundError(f"No SecurityTXT File found on this url: {url}")

    def _get_possible_file_urls(self, base_url: str) -> List[str]:
        """
        Returns all the possible urls where a security.txt could be located according to the draft RFC, section 4.
        If strict_url has been set, it simply returns the given URL.
        :param base_url: The base url.
        :return: A list of URLS where the security.txt could be located. If strict_url is True, it returns a list
        containing only the given url.
        """
        if self.strict_url:
            return [base_url]
        normalized_url = self._normalize_url(base_url)
        parsed_url = urlparse(normalized_url)
        return [f"{scheme}://{parsed_url.netloc}{path}"
                for path in self.possible_paths
                for scheme in self.possible_schemes]

    def _normalize_url(self, url: str) -> str:
        """
        Normalize a url for further processing, e.g. add slashes for urlparse
        :param url: The url to normalize
        :return: The normalized url.
        """
        return url if '//' in url else f"//{url}"

    def _parse_file_url(self, file_url: str) -> bool:
        """
        Given a URL to (possibly) a security.txt file, get the file and parse it into a securityTXT object.
        :param file_url: A URL to location where a security.txt might be located.
        :returns True if a file has been found and parsed. False otherwise.
        :raises AttributeError: if the file could not be parsed.
        """
        try:
            file = self._get_file(file_url)
            self.securitytxt = FileParser(file).securitytxt
            self.securitytxt.source_url = file_url
            return True
        except exceptions.RequestException:
            return False

    def _get_file(self, url: str) -> str:
        """
        Get a file from the URL and check if it could be a security.txt file.
        :param url: A URL to location where a security.txt might be located.
        :return: The text of a security.txt
        :raises ConnectionError: If the URL does not contain a security.txt
        """
        response = get(url, headers=self.headers, allow_redirects=True)
        if not response.ok:
            raise ConnectionError(f"Url {url} returned non-successful status code {response.status_code}")
        if '<htm' in response.text:
            raise ConnectionError(f"Url {url} returned an HTML-page")
        return response.text

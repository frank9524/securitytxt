from datetime import datetime, timezone
from typing import List, Union, Optional


class SecurityTXT:
    """The representation of a security.txt file.

    Attributes:
        raw: the raw text of the securitytxt.
        source_url: the url where the securitytxt was found, if the file is retrieved from the internet.
        contact: list if contacts provided in the security.txt file.
        expires: expiry date of the security.txt (if available, None otherwise)
        encryption: list of urls to public keys as provided in the security.txt file
        acknowledgement: list of urls to acknowledgement pages as provided in the security.txt file
        preferred_languages: list of preferred languages for contact as provided in security.txt file
        canonical: list of canonical urls as provided in security.txt file
        policy: list of urls to policies as provided in the security.txt file
        hiring: list of urls to job advertisement pages as provided in the security.txt file
        comments: list of comment lines in the security.txt file
        signature: the PGP signature of the file, (if available, None otherwise)

    Public methods:
        from_url: Retrieve and parse a security.txt file from a given url (static method)
        from_file: Parse a given security.txt file (static method)
        add_field: Add a field (key/value pair) to the securitytxt object
        is_valid: Checks if securitytxt file is considered valid according to the draft RFC.
        required_fields_present: Checks if the fields required according to the draft RFC are non-empty
        canonical_url: Checks if a given url is in the list of canonical urls
        expired: Checks if a security.txt has expired according to the specified expiry date.
    """

    def __init__(self, raw: str = "", source_url: str = None, contact: List[str] = None, expires: datetime = None,
                 encryption: List[str] = None, acknowledgement: List[str] = None, preferred_languages: List[str] = None,
                 canonical: List[str] = None, policy: List[str] = None, hiring: List[str] = None,
                 comments: List[str] = None, signature: Optional[str] = None):
        """Initialize all variables"""
        self.raw: str = raw
        self.source_url: str = source_url
        self.contact: List[str] = contact if contact else []
        self.expires: datetime = expires
        self.encryption: List[str] = encryption if encryption else []
        self.acknowledgments: List[str] = acknowledgement if acknowledgement else []
        self.preferred_languages: List[str] = preferred_languages if preferred_languages else []
        self.canonical: List[str] = canonical if canonical else []
        self.policy: List[str] = policy if policy else []
        self.hiring: List[str] = hiring if hiring else []
        self.comments: List[str] = comments if comments else []
        self.signature: Optional[str] = signature

    @property
    def expired(self) -> bool:
        """
        Whether the security.txt has expired. If the expiry date has not been set, it will return False.
        :return: Boolean indicating whether the expiry date has been set
        """
        return not self.expires or self.expires.astimezone(timezone.utc) < datetime.now().astimezone(timezone.utc)

    def canonical_url(self, url: str = None) -> bool:
        """
        Determines whether a url is in the list of canonical urls. If no url is given, the source_url of the securitytxt
        will be used. If neither are present, this function returns True. If the list of canonical URLs is empty, it
        will also return True.
        :param url: (optional) A URL to check for whether it is in the list of canonical urls
        :return: True if canonical is empty, url is empty or if the url is in list of canonical urls.
        """
        url = url if url else self.source_url
        return not url or not self.canonical or url in self.canonical

    def required_fields_present(self) -> bool:
        """
        Determines whether all the fields required in a securitytxt are non-empty
        :return: Boolean indicating whether all required fields are non-empty
        """
        return bool(self.contact) and bool(self.expires)

    def is_valid(self, url: str = None) -> bool:
        """
        Whether the securitytxt is valid according to the specification
        :param url: (optional) the url where the securitytxt was found. If not given, the attribute source_url is used.
        If neither of these are present, the checks for the url is ignored.
        :return: A boolean indicating whether the securitytxt is valid according to the specification
        """
        return self.required_fields_present() and not self.expired and self.canonical_url(url)

    def add_field(self, key: str, value: Union[str, datetime]) -> None:
        """
        Add a field value to the securitytxt
        :param key: The key of the field
        :param value: The value of the field
        """
        if not hasattr(self, key):
            self.__setattr__(key, [value])
        elif (type(getattr(self, key)) is not list) or (type(value) is list):
            self.__setattr__(key, value)
        else:
            getattr(self, key).append(value)

    @staticmethod
    def from_url(url: str, strict_url: bool = False) -> 'SecurityTXT':
        """
        Retrieve and parse a securitytxt from a given url. Unless strict_url is set, it will also look for the securitytxt
        at paths that are allowed according to the specification, such as /.well-known/security.txt
        :param url: The url from which to retrieve the securitytxt
        :param strict_url: Set to True to only look at the url specified, not any subpaths like '.well-known/security.txt'
        :return: A SecurityTXT object, that represents the securitytxt found.
        :raises
        """
        from securitytxt.parsers.url_parser import URLParser
        return URLParser(url, strict_url).securitytxt

    @staticmethod
    def from_text(text: str) -> 'SecurityTXT':
        """
        Parse a securitytxt from a text string.
        :param text: The text of the security.txt file
        :return: A SecurityTXT object, that represents the securitytxt found.
        :raises AttributeError: if the file does not have a valid format.
        """
        from securitytxt.parsers.file_parser import FileParser
        return FileParser(text).securitytxt

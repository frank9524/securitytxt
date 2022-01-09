from re import compile
from typing import Pattern

from typing import Optional


class SignedTextParser:
    """A parser to split a signature from the body of the text. The parsed values can accessed through the
    'signature' and 'unsigned_text' attributes. Creating an object of the parser immediately parses the given file.

    Attributes:
        :class signed_text_identifier: If this identifier is contained in the text, the text can be assumed to be signed
        :class signature_group_name: The regex group name for the signature
        :class unsigned_text_group_name: The regex group name for the unsigned body of the text
        signed_text: The signed text to parse

    Public methods:
        is_signed_text: determines whether the given text is signed (static method)

    Raises:
        :raises AttributeError: if the signature could not be parsed.
    """
    signed_text_identifier: str = '-----BEGIN PGP SIGNED MESSAGE-----'

    signature_group_name: str = 'signature'
    unsigned_text_group_name: str = 'unsigned_text'

    def __init__(self, signed_text: str):
        """
        Initialize variables and run the parser
        :param signed_text: The signed text to parse
        :raises AttributeError: if the signature could not be parsed.
        """
        self.signature: Optional[str] = None
        self.unsigned_text: Optional[str] = None
        self._parse(signed_text)

    @staticmethod
    def is_signed_text(text: str) -> bool:
        """
        Determine whether the text is PGP-signed according to rfc4880#section-7
        :param text: a possibly signed text
        :return: True if the document is signed, False otherwise
        """
        return text.strip(' \n').startswith(SignedTextParser.signed_text_identifier)

    def _parse(self, signed_text: str) -> None:
        """
        Parse the signed text
        :param signed_text: The signed text to parse
        :raises AttributeError: if the signature could not be parsed.
        """
        match = self._pattern.search(signed_text)
        if not match:
            raise AttributeError("The signature could not be parsed")
        groups = match.groupdict()
        self.signature = groups[self.signature_group_name].strip()
        self.unsigned_text = groups[self.unsigned_text_group_name].strip()

    @property
    def _pattern(self) -> Pattern[str]:
        """
        The regex pattern to parse a signed text. This regex is slightly more lenient than the rules specified in
        rfc4880#section-7, to accommodate for typographical errors and different file formats. It contains two groups:
        one for the signature and one for the unsigned text.
        :return: The regex pattern to parse a PGP signed text
        """
        return compile(rf"-----BEGIN PGP SIGNED MESSAGE-----\n(Hash: .*\n)?"
                       rf"(?P<{self.unsigned_text_group_name}>[\s\S]*)"
                       rf"-----BEGIN PGP SIGNATURE-----\n"
                       rf"(?P<{self.signature_group_name}>[\s\S]*)\n"
                       rf"-----END PGP SIGNATURE-----")

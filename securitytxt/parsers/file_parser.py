from securitytxt.parsers.textparsers.comment_line_parser import CommentLineParser
from securitytxt.parsers.textparsers.field_line_parser import FieldLineParser
from securitytxt.parsers.textparsers.signed_text_parser import SignedTextParser
from securitytxt.securitytxt import SecurityTXT


class FileParser:
    """Takes a security.txt file and parses it. Creating an object of the parser immediately parses the given file.

    Attributes:
        securitytxt: the resulting securitytxt after parsing.

    Public methods:
        None

    Raises:
        :raises AttributeError: if the format of the file is invalid.
    """
    def __init__(self, text: str):
        """
        Initialize SecurityTXT and run the parser to fill this object
        :param text: The text to parse
        :raises AttributeError: if the file does not has an incorrect format.
        """
        self.securitytxt: SecurityTXT = SecurityTXT(raw=text)
        self._parse(text)

    def _parse(self, text) -> SecurityTXT:
        """
        The function to parse the security.txt file. It follows the ABNF grammar specified in section 5 of the draft RFC
        :param text: The text to parse
        :return: The SecurityTXT object representing the file
        :raises AttributeError: if the file does not has an incorrect format.
        """
        # Grammar: body =  signed / unsigned
        text = self._normalize(text)
        self._parse_signed(text) if SignedTextParser.is_signed_text(text) else self._parse_unsigned(text)
        return self.securitytxt

    def _normalize(self, text: str) -> str:
        """
        Normalize the text for further processing. For example, replacing CRLF by LF
        :param text: The text to normalize
        :return: The normalized text
        """
        return text.replace('\r\n', '\n')

    def _parse_signed(self, signed_text: str) -> None:
        """
        Parse a signed text and set the values in the securitytxt attribute
        :param signed_text: the signed text to parse
        :raises AttributeError: if the signed_text is not a valid signed file.
        """
        signed_text_parser = SignedTextParser(signed_text)
        self.securitytxt.signature = signed_text_parser.signature
        self._parse_unsigned(signed_text_parser.unsigned_text)

    def _parse_unsigned(self, unsigned_text: str) -> None:
        """
        Parse an unsigned security.txt file
        :param unsigned_text: the unsigned text to parse
        """
        for line in unsigned_text.splitlines():
            self._parse_line(line)

    def _parse_line(self, line: str) -> None:
        """
        Parse a line in a security.txt file
        :param line: a line from the file
        """
        if FieldLineParser.is_field(line):
            self._parse_field(line)
        elif CommentLineParser.is_comment(line):
            self._parse_comment(line)

    def _parse_field(self, line: str) -> None:
        """
        Parse a field line
        :param line: The line to parse
        """
        try:
            field = FieldLineParser(line)
            self.securitytxt.add_field(field.key, field.value)
        except AttributeError:
            pass

    def _parse_comment(self, line: str) -> None:
        """
        Parse a comment
        :param line: The comment
        """
        comment = CommentLineParser(line)
        self.securitytxt.comments.append(comment.comment)

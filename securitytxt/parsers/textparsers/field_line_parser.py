from datetime import datetime, timezone
from typing import Union, List, Optional

from dateutil.parser import parse

from securitytxt.parsers.textparsers.comment_line_parser import CommentLineParser


class FieldLineParser:
    """A parser to parse lines containing a field, that is, a key value pair. The parsed values can accessed through the
    'key' and 'value' attributes. Creating an object of the parser immediately parses the given line.

    Attributes:
        :class field_separator The separator between the key and the value.
        :class uri_fields The fields containing a URI-value.
        :class datetime_fields The fields containing a datetime value.
        :class csv_fields: The fields containing a comma-separated value.
        key: the key of the parsed field
        value: the value of the parsed field

    Public methods:
        is_field: determines whether the given line is a field (static method)
    """
    field_separator: str = ':'

    uri_fields = ['contact', 'encryption', 'acknowledgments', 'canonical', 'policy', 'hiring']
    datetime_fields = ['expires']
    csv_fields = ['preferred_languages']

    def __init__(self, field_line: str):
        """Initialize all the values, launch the parser and checks validity of the resulting keys/values."""
        self.key: Optional[str] = None
        self.value: Optional[Union[str, datetime]] = None
        self._parse(field_line)
        self._is_valid()

    def _parse(self, field_line: str) -> None:
        """
        Parse the line containing the field (key/value pair). It finds the corresponding parse_* function and calls that
        parser for the value type.
        :param field_line: The line
        """
        key, value = field_line.split(self.field_separator, 1)
        key = self._normalize_key(key)
        if key in self.uri_fields:
            self._parse_uri_field(key, value)
        elif key in self.datetime_fields:
            self._parse_datetime_field(key, value)
        elif key in self.csv_fields:
            self._parse_csv_field(key, value)
        else:
            self._parse_unknown_field(key, value)

    def _normalize_key(self, key: str) -> str:
        """Normalize the given key, so it can be an attribute of the securitytxt class."""
        return key.lower().strip().replace('-', '_')

    def _parse_uri_field(self, key: str, value: str) -> None:
        """Parse a field where the value is a URI."""
        self.key = key
        self.value: str = value.strip()

    def _parse_datetime_field(self, key: str, value: str) -> None:
        """Parse a field where the value is a date and time."""
        self.key = key
        self.value: datetime = parse(value).astimezone(tz=timezone.utc)

    def _parse_csv_field(self, key: str, value: str) -> None:
        """Parse a field where the value is a comma separated list."""
        self.key = key
        self.value: List = list(map(str.strip, value.split(',')))

    def _parse_unknown_field(self, key: str, value: str) -> None:
        """Parse a field where the value is an unknown string."""
        self.key = key
        self.value = value

    def _is_valid(self) -> None:
        """
        Check if the key and value are valid values to be set on the securitytxt.
        :raises AttributeError: If the key and/or value is empty.
        """
        if not self.key or not self.value:
            raise AttributeError("Invalid input: either key or value is empty")

    @staticmethod
    def is_field(line: str) -> bool:
        """
        Determine whether the line is a field.
        :param line: a line from the file.
        :return: True if the line is a field, False otherwise.
        """
        return not CommentLineParser.is_comment(line) and FieldLineParser.field_separator in line

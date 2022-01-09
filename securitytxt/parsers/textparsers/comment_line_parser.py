from typing import Optional


class CommentLineParser:
    """A parser to parse lines containing a comment. The parsed values can accessed through the
    'comment' attribute. Creating an object of the parser immediately parses the given line.

    Attributes:
        :class comment_identifier If the line starts with this identifier, it can be assumed to be a comment
        comment: the parsed comment

    Public methods:
        is_comment: determines whether the given line is a comment (static method)
    """
    comment_identifier: str = '#'

    def __init__(self, comment_line: str):
        """Initialize the values and launch the parser."""
        self.comment: Optional[str] = None
        self.parse(comment_line)

    def parse(self, comment_line: str):
        """
        Parse the comment.
        :param comment_line: The line containing the comment.
        """
        self.comment = comment_line.lstrip(self.comment_identifier + ' ')

    @staticmethod
    def is_comment(line: str) -> bool:
        """
        Determine whether the line is a comment.
        :param line: a line from the file.
        :return: True if the line is a comment, False otherwise.
        """
        return line.lstrip().startswith(CommentLineParser.comment_identifier)

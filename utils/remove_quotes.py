from typing import Any

def remove_quotes(s: str, l: int, t: ParseResults) -> Any:
    r"""
    Helper parse action for removing quotation marks from parsed
    quoted strings, that use a single character for quoting. For parsing
    strings that may have multiple characters, use the :class:`QuotedString`
    class.

    Example:

    .. doctest::

       >>> # by default, quotation marks are included in parsed results
       >>> quoted_string.parse_string("'Now is the Winter of our Discontent'")
       ParseResults(["'Now is the Winter of our Discontent'"], {})

       >>> # use remove_quotes to strip quotation marks from parsed results
       >>> dequoted = quoted_string().set_parse_action(remove_quotes)
       >>> dequoted.parse_string("'Now is the Winter of our Discontent'")
       ParseResults(['Now is the Winter of our Discontent'], {})
    """
    return t[0][1:-1]


def removeQuotes(s, l, t):
    """Helper parse action for removing quotation marks from parsed
    quoted strings.

    Example::

        # by default, quotation marks are included in parsed results
        quotedString.parseString("'Now is the Winter of our Discontent'") # -> ["'Now is the Winter of our Discontent'"]

        # use removeQuotes to strip quotation marks from parsed results
        quotedString.setParseAction(removeQuotes)
        quotedString.parseString("'Now is the Winter of our Discontent'") # -> ["Now is the Winter of our Discontent"]
    """
    return t[0][1:-1]


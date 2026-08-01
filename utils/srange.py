
def srange(s: str) -> str:
    r"""Helper to easily define string ranges for use in :class:`Word`
    construction. Borrows syntax from regexp ``'[]'`` string range
    definitions::

        srange("[0-9]")   -> "0123456789"
        srange("[a-z]")   -> "abcdefghijklmnopqrstuvwxyz"
        srange("[a-z$_]") -> "abcdefghijklmnopqrstuvwxyz$_"

    The input string must be enclosed in []'s, and the returned string
    is the expanded character set joined into a single string. The
    values enclosed in the []'s may be:

    - a single character
    - an escaped character with a leading backslash (such as ``\-``
      or ``\]``)
    - an escaped hex character with a leading ``'\x'``
      (``\x21``, which is a ``'!'`` character) (``\0x##``
      is also supported for backwards compatibility)
    - an escaped octal character with a leading ``'\0'``
      (``\041``, which is a ``'!'`` character)
    - a range of any of the above, separated by a dash (``'a-z'``,
      etc.)
    - any combination of the above (``'aeiouy'``,
      ``'a-zA-Z0-9_$'``, etc.)
    """

    def _expanded(p):
        if isinstance(p, ParseResults):
            yield from (chr(c) for c in range(ord(p[0]), ord(p[1]) + 1))
        else:
            yield p

    try:
        return "".join(
            [c for part in _reBracketExpr.parse_string(s).body for c in _expanded(part)]
        )
    except Exception as e:
        return ""


def srange(s):
    r"""Helper to easily define string ranges for use in Word
    construction. Borrows syntax from regexp '[]' string range
    definitions::

        srange("[0-9]")   -> "0123456789"
        srange("[a-z]")   -> "abcdefghijklmnopqrstuvwxyz"
        srange("[a-z$_]") -> "abcdefghijklmnopqrstuvwxyz$_"

    The input string must be enclosed in []'s, and the returned string
    is the expanded character set joined into a single string. The
    values enclosed in the []'s may be:

     - a single character
     - an escaped character with a leading backslash (such as ``\-``
       or ``\]``)
     - an escaped hex character with a leading ``'\x'``
       (``\x21``, which is a ``'!'`` character) (``\0x##``
       is also supported for backwards compatibility)
     - an escaped octal character with a leading ``'\0'``
       (``\041``, which is a ``'!'`` character)
     - a range of any of the above, separated by a dash (``'a-z'``,
       etc.)
     - any combination of the above (``'aeiouy'``,
       ``'a-zA-Z0-9_$'``, etc.)
    """
    _expanded = lambda p: p if not isinstance(p, ParseResults) else ''.join(unichr(c) for c in range(ord(p[0]), ord(p[1]) + 1))
    try:
        return "".join(_expanded(part) for part in _reBracketExpr.parseString(s).body)
    except Exception:
        return ""


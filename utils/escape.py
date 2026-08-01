
def escape(s: t.Any, /) -> Markup:
    """Replace the characters ``&``, ``<``, ``>``, ``'``, and ``"`` in
    the string with HTML-safe sequences. Use this if you need to display
    text that might contain such characters in HTML.

    If the object has an ``__html__`` method, it is called and the
    return value is assumed to already be safe for HTML.

    :param s: An object to be converted to a string and escaped.
    :return: A :class:`Markup` string with the escaped text.
    """
    # If the object is already a plain string, skip __html__ check and string
    # conversion. This is the most common use case.
    # Use type(s) instead of s.__class__ because a proxy object may be reporting
    # the __class__ of the proxied value.
    if type(s) is str:
        return Markup(_escape_inner(s))

    if hasattr(s, "__html__"):
        return Markup(s.__html__())

    return Markup(_escape_inner(str(s)))


def escape(pattern, special_only=True, literal_spaces=False):
    """Escape a string for use as a literal in a pattern. If special_only is
    True, escape only special characters, else escape all non-alphanumeric
    characters. If literal_spaces is True, don't escape spaces."""
    # Convert it to Unicode.
    if isinstance(pattern, bytes):
        p = pattern.decode("latin-1")
    else:
        p = pattern

    s = []
    if special_only:
        for c in p:
            if c == " " and literal_spaces:
                s.append(c)
            elif c in _METACHARS or c.isspace():
                s.append("\\")
                s.append(c)
            else:
                s.append(c)
    else:
        for c in p:
            if c == " " and literal_spaces:
                s.append(c)
            elif c in _ALNUM:
                s.append(c)
            else:
                s.append("\\")
                s.append(c)

    r = "".join(s)
    # Convert it back to bytes if necessary.
    if isinstance(pattern, bytes):
        r = r.encode("latin-1")

    return r


def escape(
    markup: str,
    _escape: _EscapeSubMethod = re.compile(r"(\\*)(\[[a-z#/@][^[]*?])").sub,
) -> str:
    """Escapes text so that it won't be interpreted as markup.

    Args:
        markup (str): Content to be inserted in to markup.

    Returns:
        str: Markup with square brackets escaped.
    """

    def escape_backslashes(match: Match[str]) -> str:
        """Called by re.sub replace matches."""
        backslashes, text = match.groups()
        return f"{backslashes}{backslashes}\\{text}"

    markup = _escape(escape_backslashes, markup)
    if markup.endswith("\\") and not markup.endswith("\\\\"):
        return markup + "\\"

    return markup


def escape(pathname):
    """Escape all special characters."""
    # Escaping is done by wrapping any of "*?[" between square brackets.
    # Metacharacters do not work in the drive part and shouldn't be escaped.
    drive, pathname = os.path.splitdrive(pathname)
    if isinstance(pathname, bytes):
        pathname = magic_check_bytes.sub(rb'[\1]', pathname)
    else:
        pathname = magic_check.sub(r'[\1]', pathname)
    return drive + pathname


def escape(n):
    return json.dumps(n)


def escape(
    markup: str,
    _escape: _EscapeSubMethod = re.compile(r"(\\*)(\[[a-z#/@][^[]*?])").sub,
) -> str:
    """Escapes text so that it won't be interpreted as markup.

    Args:
        markup (str): Content to be inserted in to markup.

    Returns:
        str: Markup with square brackets escaped.
    """

    def escape_backslashes(match: Match[str]) -> str:
        """Called by re.sub replace matches."""
        backslashes, text = match.groups()
        return f"{backslashes}{backslashes}\\{text}"

    markup = _escape(escape_backslashes, markup)
    if markup.endswith("\\") and not markup.endswith("\\\\"):
        return markup + "\\"

    return markup


def escape(text):
    """Use XML character references to escape characters.

    Use XML character references for unprintable or non-ASCII
    characters, double quotes and ampersands in a string
    """

    def fixup(m):
        ch = m.group(0)
        return "&#" + str(ord(ch)) + ";"

    text = re.sub('[^ -~]|[&"]', fixup, text)
    return text if isinstance(text, str) else str(text)


def escape(state: StateInline, silent: bool) -> bool:
    """Process escaped chars and hardbreaks."""
    pos = state.pos
    maximum = state.posMax

    if state.src[pos] != "\\":
        return False

    pos += 1

    # '\' at the end of the inline block
    if pos >= maximum:
        return False

    ch1 = state.src[pos]
    ch1_ord = ord(ch1)
    if ch1 == "\n":
        if not silent:
            state.push("hardbreak", "br", 0)
        pos += 1
        # skip leading whitespaces from next line
        while pos < maximum:
            ch = state.src[pos]
            if not isStrSpace(ch):
                break
            pos += 1

        state.pos = pos
        return True

    escapedStr = state.src[pos]

    if ch1_ord >= 0xD800 and ch1_ord <= 0xDBFF and pos + 1 < maximum:
        ch2 = state.src[pos + 1]
        ch2_ord = ord(ch2)
        if ch2_ord >= 0xDC00 and ch2_ord <= 0xDFFF:
            escapedStr += ch2
            pos += 1

    origStr = "\\" + escapedStr

    if not silent:
        token = state.push("text_special", "", 0)
        token.content = escapedStr if ch1 in _ESCAPED else origStr
        token.markup = origStr
        token.info = "escape"

    state.pos = pos + 1
    return True


def escape(data):
    """Escape characters not allowed in `XML 1.0 <https://www.w3.org/TR/xml/#NT-Char>`_."""
    data = tostr(data, "utf_8")
    data = data.replace("&", "&amp;")
    data = data.replace("<", "&lt;")
    data = data.replace(">", "&gt;")
    data = data.replace("\r", "&#13;")

    newData = data.translate(ILLEGAL_XML_CHARS)
    if newData != data:
        maxLen = 10
        preview = repr(data)
        if len(data) > maxLen:
            preview = repr(data[:maxLen])[1:-1] + "..."
        TTX_LOG.warning(
            "Illegal XML character(s) found; replacing offending string %r with %r",
            preview,
            REPLACEMENT,
        )
    return newData


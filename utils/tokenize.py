
def tokenize(*args: Any, **kwargs: Any) -> str:
    """Deterministic token

    (modified from dask.base)

    >>> tokenize([1, 2, '3'])
    '9d71491b50023b06fc76928e6eddb952'

    >>> tokenize('Hello') == tokenize('Hello')
    True
    """
    if kwargs:
        args += (kwargs,)
    try:
        h = md5(str(args).encode())
    except ValueError:
        # FIPS systems: https://github.com/fsspec/filesystem_spec/issues/380
        h = md5(str(args).encode(), usedforsecurity=False)
    return h.hexdigest()


def tokenize(state: StateInline, silent: bool) -> bool:
    """Parse a ~subscript~ token."""
    start = state.pos
    ch = state.src[start]
    maximum = state.posMax
    found = False

    # Don't run any pairs in validation mode
    if silent:
        return False

    if ch != TILDE_CHAR:
        return False

    if start + 2 >= maximum:
        return False

    state.pos = start + 1

    while state.pos < maximum:
        if state.src[state.pos] == TILDE_CHAR:
            found = True
            break
        state.md.inline.skipToken(state)

    if not found or start + 1 == state.pos:
        state.pos = start
        return False

    content = state.src[start + 1 : state.pos]

    # Don't allow unescaped spaces/newlines inside
    if WHITESPACE_RE.search(content) is not None:
        state.pos = start
        return False

    # Found a valid pair, so update posMax and pos
    state.posMax = state.pos
    state.pos = start + 1

    # Earlier we checked "not silent", but this implementation does not need it
    token = state.push("sub_open", "sub", 1)
    token.markup = TILDE_CHAR

    token = state.push("text", "", 0)
    token.content = UNESCAPE_RE.sub(r"\1", content)

    token = state.push("sub_close", "sub", -1)
    token.markup = TILDE_CHAR

    state.pos = state.posMax + 1
    state.posMax = maximum
    return True


def tokenize(state: StateInline, silent: bool) -> bool:
    """Insert each marker as a separate text token, and add it to delimiter list"""
    start = state.pos
    marker = state.src[start]

    if silent:
        return False

    if marker not in ("_", "*"):
        return False

    scanned = state.scanDelims(state.pos, marker == "*")

    for _ in range(scanned.length):
        token = state.push("text", "", 0)
        token.content = marker
        state.delimiters.append(
            Delimiter(
                marker=ord(marker),
                length=scanned.length,
                token=len(state.tokens) - 1,
                end=-1,
                open=scanned.can_open,
                close=scanned.can_close,
            )
        )

    state.pos += scanned.length

    return True


def tokenize(state: StateInline, silent: bool) -> bool:
    """Insert each marker as a separate text token, and add it to delimiter list.

    When the ``strikethrough_single_tilde`` option is enabled on the
    ``MarkdownIt`` instance, single ``~`` delimiters are also accepted and
    runs of three or more tildes are rejected (matching GitHub's rendering behaviour).
    """
    start = state.pos
    ch = state.src[start]

    if silent:
        return False

    if ch != "~":
        return False

    scanned = state.scanDelims(state.pos, True)
    length = scanned.length

    single_tilde = state.md.options.get("strikethrough_single_tilde", False)

    if single_tilde:
        # GitHub mode: only accept exactly 1 or 2 tildes.
        if length < 1:
            return False
        if length > 2:
            # Consume 3+ tildes as plain text so the parser doesn't
            # re-enter and match a subset of them.  This intentionally
            # matches GitHub's rendering, where ≥3 tildes are literal text.
            token = state.push("text", "", 0)
            token.content = ch * length
            state.pos += scanned.length
            return True

        token = state.push("text", "", 0)
        token.content = ch * length
        state.delimiters.append(
            Delimiter(
                marker=ord(ch),
                length=0,  # disable "rule of 3" length checks
                token=len(state.tokens) - 1,
                end=-1,
                open=scanned.can_open,
                close=scanned.can_close,
            )
        )
    else:
        # Original markdown-it behaviour: minimum 2, split odd runs.
        if length < 2:
            return False

        if length % 2:
            token = state.push("text", "", 0)
            token.content = ch
            length -= 1

        i = 0
        while i < length:
            token = state.push("text", "", 0)
            token.content = ch + ch
            state.delimiters.append(
                Delimiter(
                    marker=ord(ch),
                    length=0,  # disable "rule of 3" length checks
                    token=len(state.tokens) - 1,
                    end=-1,
                    open=scanned.can_open,
                    close=scanned.can_close,
                )
            )

            i += 2

    state.pos += scanned.length

    return True


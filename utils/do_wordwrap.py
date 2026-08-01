
def do_wordwrap(
    environment: "Environment",
    s: str,
    width: int = 79,
    break_long_words: bool = True,
    wrapstring: t.Optional[str] = None,
    break_on_hyphens: bool = True,
) -> str:
    """Wrap a string to the given width. Existing newlines are treated
    as paragraphs to be wrapped separately.

    :param s: Original text to wrap.
    :param width: Maximum length of wrapped lines.
    :param break_long_words: If a word is longer than ``width``, break
        it across lines.
    :param break_on_hyphens: If a word contains hyphens, it may be split
        across lines.
    :param wrapstring: String to join each wrapped line. Defaults to
        :attr:`Environment.newline_sequence`.

    .. versionchanged:: 2.11
        Existing newlines are treated as paragraphs wrapped separately.

    .. versionchanged:: 2.11
        Added the ``break_on_hyphens`` parameter.

    .. versionchanged:: 2.7
        Added the ``wrapstring`` parameter.
    """
    import textwrap

    if wrapstring is None:
        wrapstring = environment.newline_sequence

    # textwrap.wrap doesn't consider existing newlines when wrapping.
    # If the string has a newline before width, wrap will still insert
    # a newline at width, resulting in a short line. Instead, split and
    # wrap each paragraph individually.
    return wrapstring.join(
        [
            wrapstring.join(
                textwrap.wrap(
                    line,
                    width=width,
                    expand_tabs=False,
                    replace_whitespace=False,
                    break_long_words=break_long_words,
                    break_on_hyphens=break_on_hyphens,
                )
            )
            for line in s.splitlines()
        ]
    )


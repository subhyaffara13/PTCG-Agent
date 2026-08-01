
def clean(
    text,
    tags=ALLOWED_TAGS,
    attributes=ALLOWED_ATTRIBUTES,
    protocols=ALLOWED_PROTOCOLS,
    strip=False,
    strip_comments=True,
    css_sanitizer=None,
):
    """Clean an HTML fragment of malicious content and return it

    This function is a security-focused function whose sole purpose is to
    remove malicious content from a string such that it can be displayed as
    content in a web page.

    This function is not designed to use to transform content to be used in
    non-web-page contexts.

    Example::

        import bleach

        better_text = bleach.clean(yucky_text)


    .. Note::

       If you're cleaning a lot of text and passing the same argument values or
       you want more configurability, consider using a
       :py:class:`bleach.sanitizer.Cleaner` instance.

    :arg str text: the text to clean

    :arg set tags: set of allowed tags; defaults to
        ``bleach.sanitizer.ALLOWED_TAGS``

    :arg dict attributes: allowed attributes; can be a callable, list or dict;
        defaults to ``bleach.sanitizer.ALLOWED_ATTRIBUTES``

    :arg set protocols: set of allowed protocols for links; defaults
        to ``bleach.sanitizer.ALLOWED_PROTOCOLS``

    :arg bool strip: whether or not to strip disallowed elements

    :arg bool strip_comments: whether or not to strip HTML comments

    :arg CSSSanitizer css_sanitizer: instance with a "sanitize_css" method for
        sanitizing style attribute values and style text; defaults to None

    :returns: cleaned text as unicode

    """
    cleaner = Cleaner(
        tags=tags,
        attributes=attributes,
        protocols=protocols,
        strip=strip,
        strip_comments=strip_comments,
        css_sanitizer=css_sanitizer,
    )
    return cleaner.clean(text)


def clean(lines: Iterable[str]):
    """
    Yield non-blank, non-comment elements from lines.
    """
    return filter(_nonblank, map(str.strip, lines))


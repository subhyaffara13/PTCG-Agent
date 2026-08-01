
def get_content_type(mimetype: str, charset: str) -> str:
    """Returns the full content type string with charset for a mimetype.

    If the mimetype represents text, the charset parameter will be
    appended, otherwise the mimetype is returned unchanged.

    :param mimetype: The mimetype to be used as content type.
    :param charset: The charset to be appended for text mimetypes.
    :return: The content type.

    .. versionchanged:: 0.15
        Any type that ends with ``+xml`` gets a charset, not just those
        that start with ``application/``. Known text types such as
        ``application/javascript`` are also given charsets.
    """
    if (
        mimetype.startswith("text/")
        or mimetype in _charset_mimetypes
        or mimetype.endswith("+xml")
    ):
        mimetype += f"; charset={charset}"

    return mimetype


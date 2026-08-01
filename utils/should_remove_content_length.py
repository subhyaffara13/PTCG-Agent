
def should_remove_content_length(method: str, code: int) -> bool:
    """Check if a Content-Length header should be removed.

    This should always be a subset of must_be_empty_body
    """
    # https://www.rfc-editor.org/rfc/rfc9110.html#section-8.6-8
    # https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4.5-4
    return code in EMPTY_BODY_STATUS_CODES or (
        200 <= code < 300 and method in hdrs.METH_CONNECT_ALL
    )


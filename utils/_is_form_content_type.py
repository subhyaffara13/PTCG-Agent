
def _is_form_content_type(content_type: str) -> bool:
    """
    True iff Starlette's ``request.form()`` will actually parse this body.

    Substring matching ``"form"`` is unsafe: ``request.form()`` returns empty
    ``FormData`` for non-canonical types without consuming the body, leaving
    the auth-time pre-read and the handler's read seeing different payloads.
    """
    return _normalize_media_type(content_type) in _FORM_CONTENT_TYPES


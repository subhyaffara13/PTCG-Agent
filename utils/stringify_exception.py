
def stringify_exception(
    exc: BaseException, include_subexception_msg: bool = True
) -> str:
    try:
        notes = getattr(exc, "__notes__", [])
    except KeyError:
        # Workaround for https://github.com/python/cpython/issues/98778 on
        # some 3.10 and 3.11 patch versions.
        HTTPError = getattr(sys.modules.get("urllib.error", None), "HTTPError", ())
        if sys.version_info < (3, 12) and isinstance(exc, HTTPError):
            notes = []
        else:  # pragma: no cover
            # exception not related to above bug, reraise
            raise
    if not include_subexception_msg and isinstance(exc, BaseExceptionGroup):
        message = exc.message
    else:
        message = str(exc)

    return "\n".join(
        [
            message,
            *notes,
        ]
    )


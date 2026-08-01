
def _cfg_read_utf8_with_fallback(
    cfg: RawConfigParser, file: str, fallback_encoding=py39.LOCALE_ENCODING
) -> None:
    """Same idea as :func:`_read_utf8_with_fallback`, but for the
    :meth:`RawConfigParser.read` method.

    This method may call ``cfg.clear()``.
    """
    try:
        cfg.read(file, encoding="utf-8")
    except UnicodeDecodeError:  # pragma: no cover
        _Utf8EncodingNeeded.emit(file=file, fallback_encoding=fallback_encoding)
        cfg.clear()
        cfg.read(file, encoding=fallback_encoding)


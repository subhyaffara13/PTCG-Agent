
def set_locale(
    new_locale: str | tuple[str, str], lc_var: int = locale.LC_ALL
) -> Generator[str | tuple[str, str]]:
    """
    Context manager for temporarily setting a locale.

    Parameters
    ----------
    new_locale : str or tuple
        A string of the form <language_country>.<encoding>. For example to set
        the current locale to US English with a UTF8 encoding, you would pass
        "en_US.UTF-8".
    lc_var : int, default `locale.LC_ALL`
        The category of the locale being set.

    Notes
    -----
    This is useful when you want to run a particular block of code under a
    particular locale, without globally setting the locale. This probably isn't
    thread-safe.
    """
    # getlocale is not always compliant with setlocale, use setlocale. GH#46595
    current_locale = locale.setlocale(lc_var)

    try:
        locale.setlocale(lc_var, new_locale)
        normalized_code, normalized_encoding = locale.getlocale()
        if normalized_code is not None and normalized_encoding is not None:
            yield f"{normalized_code}.{normalized_encoding}"
        else:
            yield new_locale
    finally:
        locale.setlocale(lc_var, current_locale)



def _get_flag_lookup() -> dict[str, int]:
    import doctest

    return dict(
        DONT_ACCEPT_TRUE_FOR_1=doctest.DONT_ACCEPT_TRUE_FOR_1,
        DONT_ACCEPT_BLANKLINE=doctest.DONT_ACCEPT_BLANKLINE,
        NORMALIZE_WHITESPACE=doctest.NORMALIZE_WHITESPACE,
        ELLIPSIS=doctest.ELLIPSIS,
        IGNORE_EXCEPTION_DETAIL=doctest.IGNORE_EXCEPTION_DETAIL,
        COMPARISON_FLAGS=doctest.COMPARISON_FLAGS,
        ALLOW_UNICODE=_get_allow_unicode_flag(),
        ALLOW_BYTES=_get_allow_bytes_flag(),
        NUMBER=_get_number_flag(),
    )


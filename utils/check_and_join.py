
def check_and_join(phrase, symbols=None, filter=None):
    """
    Joins characters of ``phrase`` and if ``symbols`` is given, raises
    an error if any character in ``phrase`` is not in ``symbols``.

    Parameters
    ==========

    phrase
        String or list of strings to be returned as a string.

    symbols
        Iterable of characters allowed in ``phrase``.

        If ``symbols`` is ``None``, no checking is performed.

    Examples
    ========

    >>> from sympy.crypto.crypto import check_and_join
    >>> check_and_join('a phrase')
    'a phrase'
    >>> check_and_join('a phrase'.upper().split())
    'APHRASE'
    >>> check_and_join('a phrase!'.upper().split(), 'ARE', filter=True)
    'ARAE'
    >>> check_and_join('a phrase!'.upper().split(), 'ARE')
    Traceback (most recent call last):
    ...
    ValueError: characters in phrase but not symbols: "!HPS"

    """
    rv = ''.join(''.join(phrase))
    if symbols is not None:
        symbols = check_and_join(symbols)
        missing = ''.join(sorted(set(rv) - set(symbols)))
        if missing:
            if not filter:
                raise ValueError(
                    'characters in phrase but not symbols: "%s"' % missing)
            rv = translate(rv, None, missing)
    return rv


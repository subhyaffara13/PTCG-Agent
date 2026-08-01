
def padded_key(key, symbols):
    """Return a string of the distinct characters of ``symbols`` with
    those of ``key`` appearing first. A ValueError is raised if
    a) there are duplicate characters in ``symbols`` or
    b) there are characters in ``key`` that are  not in ``symbols``.

    Examples
    ========

    >>> from sympy.crypto.crypto import padded_key
    >>> padded_key('PUPPY', 'OPQRSTUVWXY')
    'PUYOQRSTVWX'
    >>> padded_key('RSA', 'ARTIST')
    Traceback (most recent call last):
    ...
    ValueError: duplicate characters in symbols: T

    """
    syms = list(uniq(symbols))
    if len(syms) != len(symbols):
        extra = ''.join(sorted({
            i for i in symbols if symbols.count(i) > 1}))
        raise ValueError('duplicate characters in symbols: %s' % extra)
    extra = set(key) - set(syms)
    if extra:
        raise ValueError(
            'characters in key but not symbols: %s' % ''.join(
            sorted(extra)))
    key0 = ''.join(list(uniq(key)))
    # remove from syms characters in key0
    return key0 + translate(''.join(syms), None, key0)


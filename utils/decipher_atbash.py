
def decipher_atbash(msg, symbols=None):
    r"""
    Deciphers a given ``msg`` using Atbash cipher and returns it.

    Explanation
    ===========

    ``decipher_atbash`` is functionally equivalent to ``encipher_atbash``.
    However, it has still been added as a separate function to maintain
    consistency.

    Examples
    ========

    >>> from sympy.crypto.crypto import encipher_atbash, decipher_atbash
    >>> msg = 'GONAVYBEATARMY'
    >>> encipher_atbash(msg)
    'TLMZEBYVZGZINB'
    >>> decipher_atbash(msg)
    'TLMZEBYVZGZINB'
    >>> encipher_atbash(msg) == decipher_atbash(msg)
    True
    >>> msg == encipher_atbash(encipher_atbash(msg))
    True

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Atbash

    See Also
    ========

    encipher_atbash

    """
    return decipher_affine(msg, (25, 25), symbols)


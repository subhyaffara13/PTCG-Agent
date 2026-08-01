
def decipher_shift(msg, key, symbols=None):
    """
    Return the text by shifting the characters of ``msg`` to the
    left by the amount given by ``key``.

    Examples
    ========

    >>> from sympy.crypto.crypto import encipher_shift, decipher_shift
    >>> msg = "GONAVYBEATARMY"
    >>> ct = encipher_shift(msg, 1); ct
    'HPOBWZCFBUBSNZ'

    To decipher the shifted text, change the sign of the key:

    >>> encipher_shift(ct, -1)
    'GONAVYBEATARMY'

    Or use this function with the original key:

    >>> decipher_shift(ct, 1)
    'GONAVYBEATARMY'

    """
    return encipher_shift(msg, -key, symbols)


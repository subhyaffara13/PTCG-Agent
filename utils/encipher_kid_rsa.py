
def encipher_kid_rsa(msg, key):
    """
    Here ``msg`` is the plaintext and ``key`` is the public key.

    Examples
    ========

    >>> from sympy.crypto.crypto import (
    ...     encipher_kid_rsa, kid_rsa_public_key)
    >>> msg = 200
    >>> a, b, A, B = 3, 4, 5, 6
    >>> key = kid_rsa_public_key(a, b, A, B)
    >>> encipher_kid_rsa(msg, key)
    161

    """
    n, e = key
    return (msg*e) % n


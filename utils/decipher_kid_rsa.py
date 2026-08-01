
def decipher_kid_rsa(msg, key):
    """
    Here ``msg`` is the plaintext and ``key`` is the private key.

    Examples
    ========

    >>> from sympy.crypto.crypto import (
    ...     kid_rsa_public_key, kid_rsa_private_key,
    ...     decipher_kid_rsa, encipher_kid_rsa)
    >>> a, b, A, B = 3, 4, 5, 6
    >>> d = kid_rsa_private_key(a, b, A, B)
    >>> msg = 200
    >>> pub = kid_rsa_public_key(a, b, A, B)
    >>> pri = kid_rsa_private_key(a, b, A, B)
    >>> ct = encipher_kid_rsa(msg, pub)
    >>> decipher_kid_rsa(ct, pri)
    200

    """
    n, d = key
    return (msg*d) % n


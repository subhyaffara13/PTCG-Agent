
def _decipher_rsa_crt(i, d, factors):
    """Decipher RSA using chinese remainder theorem from the information
    of the relatively-prime factors of the modulus.

    Parameters
    ==========

    i : integer
        Ciphertext

    d : integer
        The exponent component.

    factors : list of relatively-prime integers
        The integers given must be coprime and the product must equal
        the modulus component of the original RSA key.

    Examples
    ========

    How to decrypt RSA with CRT:

    >>> from sympy.crypto.crypto import rsa_public_key, rsa_private_key
    >>> primes = [61, 53]
    >>> e = 17
    >>> args = primes + [e]
    >>> puk = rsa_public_key(*args)
    >>> prk = rsa_private_key(*args)

    >>> from sympy.crypto.crypto import encipher_rsa, _decipher_rsa_crt
    >>> msg = 65
    >>> crt_primes = primes
    >>> encrypted = encipher_rsa(msg, puk)
    >>> decrypted = _decipher_rsa_crt(encrypted, prk[1], primes)
    >>> decrypted
    65
    """
    moduluses = [pow(i, d, p) for p in factors]

    result = crt(factors, moduluses)
    if not result:
        raise ValueError("CRT failed")
    return result[0]


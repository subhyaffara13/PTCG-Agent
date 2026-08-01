
def encipher_railfence(message,rails):
    """
    Performs Railfence Encryption on plaintext and returns ciphertext

    Examples
    ========

    >>> from sympy.crypto.crypto import encipher_railfence
    >>> message = "hello world"
    >>> encipher_railfence(message,3)
    'horel ollwd'

    Parameters
    ==========

    message : string, the message to encrypt.
    rails : int, the number of rails.

    Returns
    =======

    The Encrypted string message.

    References
    ==========
    .. [1] https://en.wikipedia.org/wiki/Rail_fence_cipher

    """
    r = list(range(rails))
    p = cycle(r + r[-2:0:-1])
    return ''.join(sorted(message, key=lambda i: next(p)))


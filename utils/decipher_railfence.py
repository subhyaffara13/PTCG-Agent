
def decipher_railfence(ciphertext,rails):
    """
    Decrypt the message using the given rails

    Examples
    ========

    >>> from sympy.crypto.crypto import decipher_railfence
    >>> decipher_railfence("horel ollwd",3)
    'hello world'

    Parameters
    ==========

    message : string, the message to encrypt.
    rails : int, the number of rails.

    Returns
    =======

    The Decrypted string message.

    """
    r = list(range(rails))
    p = cycle(r + r[-2:0:-1])

    idx = sorted(range(len(ciphertext)), key=lambda i: next(p))
    res = [''] * len(ciphertext)
    for i, c in zip(idx, ciphertext):
        res[i] = c
    return ''.join(res)


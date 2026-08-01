
def kid_rsa_public_key(a, b, A, B):
    r"""
    Kid RSA is a version of RSA useful to teach grade school children
    since it does not involve exponentiation.

    Explanation
    ===========

    Alice wants to talk to Bob. Bob generates keys as follows.
    Key generation:

    * Select positive integers `a, b, A, B` at random.
    * Compute `M = a b - 1`, `e = A M + a`, `d = B M + b`,
      `n = (e d - 1)//M`.
    * The *public key* is `(n, e)`. Bob sends these to Alice.
    * The *private key* is `(n, d)`, which Bob keeps secret.

    Encryption: If `p` is the plaintext message then the
    ciphertext is `c = p e \pmod n`.

    Decryption: If `c` is the ciphertext message then the
    plaintext is `p = c d \pmod n`.

    Examples
    ========

    >>> from sympy.crypto.crypto import kid_rsa_public_key
    >>> a, b, A, B = 3, 4, 5, 6
    >>> kid_rsa_public_key(a, b, A, B)
    (369, 58)

    """
    M = a*b - 1
    e = A*M + a
    d = B*M + b
    n = (e*d - 1)//M
    return n, e


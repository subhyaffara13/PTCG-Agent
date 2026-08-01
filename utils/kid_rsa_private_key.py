
def kid_rsa_private_key(a, b, A, B):
    """
    Compute `M = a b - 1`, `e = A M + a`, `d = B M + b`,
    `n = (e d - 1) / M`. The *private key* is `d`, which Bob
    keeps secret.

    Examples
    ========

    >>> from sympy.crypto.crypto import kid_rsa_private_key
    >>> a, b, A, B = 3, 4, 5, 6
    >>> kid_rsa_private_key(a, b, A, B)
    (369, 70)

    """
    M = a*b - 1
    e = A*M + a
    d = B*M + b
    n = (e*d - 1)//M
    return n, d


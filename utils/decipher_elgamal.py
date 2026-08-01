
def decipher_elgamal(msg, key):
    r"""
    Decrypt message with private key.

    `msg = (c_{1}, c_{2})`

    `key = (p, r, d)`

    According to extended Eucliden theorem,
    `u c_{1}^{d} + p n = 1`

    `u \equiv 1/{{c_{1}}^d} \pmod p`

    `u c_{2} \equiv \frac{1}{c_{1}^d} c_{2} \equiv \frac{1}{r^{ad}} c_{2} \pmod p`

    `\frac{1}{r^{ad}} m e^a \equiv \frac{1}{r^{ad}} m {r^{d a}} \equiv m \pmod p`

    Examples
    ========

    >>> from sympy.crypto.crypto import decipher_elgamal
    >>> from sympy.crypto.crypto import encipher_elgamal
    >>> from sympy.crypto.crypto import elgamal_private_key
    >>> from sympy.crypto.crypto import elgamal_public_key

    >>> pri = elgamal_private_key(5, seed=[3])
    >>> pub = elgamal_public_key(pri); pub
    (37, 2, 8)
    >>> msg = 17
    >>> decipher_elgamal(encipher_elgamal(msg, pub), pri) == msg
    True

    """
    p, _, d = key
    c1, c2 = msg
    u = pow(c1, -d, p)
    return u * c2 % p


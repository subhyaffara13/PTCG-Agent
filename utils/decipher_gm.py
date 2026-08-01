
def decipher_gm(message, key):
    """
    Decrypt message 'message' using public_key 'key'.

    Parameters
    ==========

    message : list of int
        The randomized encrypted message.

    key : (p, q)
        The private key.

    Returns
    =======

    int
        The encrypted message.

    """
    p, q = key
    res = lambda m, p: _legendre(m, p) > 0
    bits = [res(m, p) * res(m, q) for m in message]
    m = 0
    for b in bits:
        m <<= 1
        m += not b
    return m


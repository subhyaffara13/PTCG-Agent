
def encipher_gm(i, key, seed=None):
    """
    Encrypt integer 'i' using public_key 'key'
    Note that gm uses random encryption.

    Parameters
    ==========

    i : int
        The message to encrypt.

    key : (a, N)
        The public key.

    Returns
    =======

    list : list of int
        The randomized encrypted message.

    """
    if i < 0:
        raise ValueError(
            "message must be a non-negative "
            "integer: got %d instead" % i)
    a, N = key
    bits = []
    while i > 0:
        bits.append(i % 2)
        i //= 2

    gen = _random_coprime_stream(N, seed)
    rev = reversed(bits)
    encode = lambda b: next(gen)**2*pow(a, b) % N
    return [ encode(b) for b in rev ]


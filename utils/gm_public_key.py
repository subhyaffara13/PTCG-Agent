
def gm_public_key(p, q, a=None, seed=None):
    """
    Compute public keys for ``p`` and ``q``.
    Note that in Goldwasser-Micali Encryption,
    public keys are randomly selected.

    Parameters
    ==========

    p, q, a : int, int, int
        Initialization variables.

    Returns
    =======

    tuple : (a, N)
        ``a`` is the input ``a`` if it is not ``None`` otherwise
        some random integer coprime to ``p`` and ``q``.

        ``N`` is the product of ``p`` and ``q``.

    """

    p, q = gm_private_key(p, q)
    N = p * q

    if a is None:
        randrange = _randrange(seed)
        while True:
            a = randrange(N)
            if _legendre(a, p) == _legendre(a, q) == -1:
                break
    else:
        if _legendre(a, p) != -1 or _legendre(a, q) != -1:
            return False
    return (a, N)



def bg_public_key(p, q):
    """
    Calculates public keys from private keys.

    Explanation
    ===========

    The function first checks the validity of
    private keys passed as arguments and
    then returns their product.

    Parameters
    ==========

    p, q
        The private keys.

    Returns
    =======

    N
        The public key.

    """
    p, q = bg_private_key(p, q)
    N = p * q
    return N


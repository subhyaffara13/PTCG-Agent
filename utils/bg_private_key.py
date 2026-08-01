
def bg_private_key(p, q):
    """
    Check if p and q can be used as private keys for
    the Blum-Goldwasser cryptosystem.

    Explanation
    ===========

    The three necessary checks for p and q to pass
    so that they can be used as private keys:

        1. p and q must both be prime
        2. p and q must be distinct
        3. p and q must be congruent to 3 mod 4

    Parameters
    ==========

    p, q
        The keys to be checked.

    Returns
    =======

    p, q
        Input values.

    Raises
    ======

    ValueError
        If p and q do not pass the above conditions.

    """

    if not isprime(p) or not isprime(q):
        raise ValueError("the two arguments must be prime, "
                         "got %i and %i" %(p, q))
    elif p == q:
        raise ValueError("the two arguments must be distinct, "
                         "got two copies of %i. " %p)
    elif (p - 3) % 4 != 0 or (q - 3) % 4 != 0:
        raise ValueError("the two arguments must be congruent to 3 mod 4, "
                         "got %i and %i" %(p, q))
    return p, q


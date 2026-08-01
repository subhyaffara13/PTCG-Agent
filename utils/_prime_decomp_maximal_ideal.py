
def _prime_decomp_maximal_ideal(I, p, ZK):
    r"""
    We have reached the case where we have a maximal (hence prime) ideal *I*,
    which we know because the quotient ``O/I`` is a field.

    Parameters
    ==========

    I : :py:class:`~.Module`
        An ideal of ``O/pO``.
    p : int
        The rational prime being factored.
    ZK : :py:class:`~.Submodule`
        The maximal order.

    Returns
    =======

    :py:class:`~.PrimeIdeal` instance representing this prime

    """
    m, n = I.matrix.shape
    f = m - n
    G = ZK.matrix * I.matrix
    gens = [ZK.parent(G[:, j], denom=ZK.denom) for j in range(G.shape[1])]
    alpha = _two_elt_rep(gens, ZK, p, f=f)
    return PrimeIdeal(ZK, p, alpha, f)


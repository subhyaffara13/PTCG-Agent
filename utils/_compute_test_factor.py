
def _compute_test_factor(p, gens, ZK):
    r"""
    Compute the test factor for a :py:class:`~.PrimeIdeal` $\mathfrak{p}$.

    Parameters
    ==========

    p : int
        The rational prime $\mathfrak{p}$ divides

    gens : list of :py:class:`PowerBasisElement`
        A complete set of generators for $\mathfrak{p}$ over *ZK*, EXCEPT that
        an element equivalent to rational *p* can and should be omitted (since
        it has no effect except to waste time).

    ZK : :py:class:`~.Submodule`
        The maximal order where the prime ideal $\mathfrak{p}$ lives.

    Returns
    =======

    :py:class:`~.PowerBasisElement`

    References
    ==========

    .. [1] Cohen, H. *A Course in Computational Algebraic Number Theory.*
    (See Proposition 4.8.15.)

    """
    _check_formal_conditions_for_maximal_order(ZK)
    E = ZK.endomorphism_ring()
    matrices = [E.inner_endomorphism(g).matrix(modulus=p) for g in gens]
    B = DomainMatrix.zeros((0, ZK.n), FF(p)).vstack(*matrices)
    # A nonzero element of the nullspace of B will represent a
    # lin comb over the omegas which (i) is not a multiple of p
    # (since it is nonzero over FF(p)), while (ii) is such that
    # its product with each g in gens _is_ a multiple of p (since
    # B represents multiplication by these generators). Theory
    # predicts that such an element must exist, so nullspace should
    # be non-trivial.
    x = B.nullspace()[0, :].transpose()
    beta = ZK.parent(ZK.matrix * x.convert_to(ZZ), denom=ZK.denom)
    return beta


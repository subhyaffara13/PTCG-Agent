
def _two_elt_rep(gens, ZK, p, f=None, Np=None):
    r"""
    Given a set of *ZK*-generators of a prime ideal, compute a set of just two
    *ZK*-generators for the same ideal, one of which is *p* itself.

    Parameters
    ==========

    gens : list of :py:class:`PowerBasisElement`
        Generators for the prime ideal over *ZK*, the ring of integers of the
        field $K$.

    ZK : :py:class:`~.Submodule`
        The maximal order in $K$.

    p : int
        The rational prime divided by the prime ideal.

    f : int, optional
        The inertia degree of the prime ideal, if known.

    Np : int, optional
        The norm $p^f$ of the prime ideal, if known.
        NOTE: There is no reason to supply both *f* and *Np*. Either one will
        save us from having to compute the norm *Np* ourselves. If both are known,
        *Np* is preferred since it saves one exponentiation.

    Returns
    =======

    :py:class:`~.PowerBasisElement` representing a single algebraic integer
    alpha such that the prime ideal is equal to ``p*ZK + alpha*ZK``.

    References
    ==========

    .. [1] Cohen, H. *A Course in Computational Algebraic Number Theory.*
    (See Algorithm 4.7.10.)

    """
    _check_formal_conditions_for_maximal_order(ZK)
    pb = ZK.parent
    T = pb.T
    # Detect the special cases in which either (a) all generators are multiples
    # of p, or (b) there are no generators (so `all` is vacuously true):
    if all((g % p).equiv(0) for g in gens):
        return pb.zero()

    if Np is None:
        if f is not None:
            Np = p**f
        else:
            Np = abs(pb.submodule_from_gens(gens).matrix.det())

    omega = ZK.basis_element_pullbacks()
    beta = [p*om for om in omega[1:]]  # note: we omit omega[0] == 1
    beta += gens
    search = coeff_search(len(beta), 1)
    for c in search:
        alpha = sum(ci*betai for ci, betai in zip(c, beta))
        # Note: It may be tempting to reduce alpha mod p here, to try to work
        # with smaller numbers, but must not do that, as it can result in an
        # infinite loop! E.g. try factoring 2 in Q(sqrt(-7)).
        n = alpha.norm(T) // Np
        if n % p != 0:
            # Now can reduce alpha mod p.
            return alpha % p


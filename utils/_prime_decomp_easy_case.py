
def _prime_decomp_easy_case(p, ZK):
    r"""
    Compute the decomposition of rational prime *p* in the ring of integers
    *ZK* (given as a :py:class:`~.Submodule`), in the "easy case", i.e. the
    case where *p* does not divide the index of $\theta$ in *ZK*, where
    $\theta$ is the generator of the ``PowerBasis`` of which *ZK* is a
    ``Submodule``.
    """
    T = ZK.parent.T
    T_bar = Poly(T, modulus=p)
    lc, fl = T_bar.factor_list()
    if len(fl) == 1 and fl[0][1] == 1:
        return [PrimeIdeal(ZK, p, ZK.parent.zero(), ZK.n, 1)]
    return [PrimeIdeal(ZK, p,
                       ZK.parent.element_from_poly(Poly(t, domain=ZZ)),
                       t.degree(), e)
            for t, e in fl]


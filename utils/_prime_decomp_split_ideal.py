
def _prime_decomp_split_ideal(I, p, N, G, ZK):
    r"""
    Perform the step in the prime decomposition algorithm where we have determined
    the quotient ``ZK/I`` is _not_ a field, and we want to perform a non-trivial
    factorization of *I* by locating an idempotent element of ``ZK/I``.
    """
    assert I.parent == ZK and G.parent is ZK and N.parent is G
    # Since ZK/I is not a field, the kernel computed in the previous step contains
    # more than just the prime field Fp, and our basis N for the nullspace therefore
    # contains at least a second column (which represents an element outside Fp).
    # Let alpha be such an element:
    alpha = N(1).to_parent()
    assert alpha.module is G

    alpha_powers = []
    m = find_min_poly(alpha, FF(p), powers=alpha_powers)
    # TODO (future work):
    #  We don't actually need full factorization, so might use a faster method
    #  to just break off a single non-constant factor m1?
    lc, fl = m.factor_list()
    m1 = fl[0][0]
    m2 = m.quo(m1)
    U, V, g = m1.gcdex(m2)
    # Sanity check: theory says m is squarefree, so m1, m2 should be coprime:
    assert g == 1
    E = list(reversed(Poly(U * m1, domain=ZZ).rep.to_list()))
    eps1 = sum(E[i]*alpha_powers[i] for i in range(len(E)))
    eps2 = 1 - eps1
    idemps = [eps1, eps2]
    factors = []
    for eps in idemps:
        e = eps.to_parent()
        assert e.module is ZK
        D = I.matrix.convert_to(FF(p)).hstack(*[
            (e * om).column(domain=FF(p)) for om in ZK.basis_elements()
        ])
        W = D.columnspace().convert_to(ZZ)
        H = ZK.submodule_from_matrix(W)
        factors.append(H)
    return factors


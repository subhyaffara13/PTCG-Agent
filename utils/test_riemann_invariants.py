
def test_riemann_invariants():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11 = \
        tensor_indices('d0:12', Lorentz)
    # R^{d0 d1}_{d1 d0}; ord = [d0,-d0,d1,-d1]
    # T_c = -R^{d0 d1}_{d0 d1}
    R = TensorHead('R', [Lorentz]*4, TensorSymmetry.riemann())
    t = R(d0, d1, -d1, -d0)
    tc = t.canon_bp()
    assert str(tc) == '-R(L_0, L_1, -L_0, -L_1)'

    # R_d11^d1_d0^d5 * R^{d6 d4 d0}_d5 * R_{d7 d2 d8 d9} *
    # R_{d10 d3 d6 d4} * R^{d2 d7 d11}_d1 * R^{d8 d9 d3 d10}
    # can = [0,2,4,6, 1,3,8,10, 5,7,12,14, 9,11,16,18, 13,15,20,22,
    #        17,19,21<F10,23, 24,25]
    # T_c = R^{d0 d1 d2 d3} * R_{d0 d1}^{d4 d5} * R_{d2 d3}^{d6 d7} *
    # R_{d4 d5}^{d8 d9} * R_{d6 d7}^{d10 d11} * R_{d8 d9 d10 d11}

    t = R(-d11,d1,-d0,d5)*R(d6,d4,d0,-d5)*R(-d7,-d2,-d8,-d9)* \
        R(-d10,-d3,-d6,-d4)*R(d2,d7,d11,-d1)*R(d8,d9,d3,d10)
    tc = t.canon_bp()
    assert str(tc) == 'R(L_0, L_1, L_2, L_3)*R(-L_0, -L_1, L_4, L_5)*R(-L_2, -L_3, L_6, L_7)*R(-L_4, -L_5, L_8, L_9)*R(-L_6, -L_7, L_10, L_11)*R(-L_8, -L_9, -L_10, -L_11)'


def test_riemann_invariants():
    baser, gensr = riemann_bsgs
    # R^{d0 d1}_{d1 d0}; ord = [d0,-d0,d1,-d1]; g = [0,2,3,1,4,5]
    # T_c = -R^{d0 d1}_{d0 d1}; can = [0,2,1,3,5,4]
    g = Permutation([0,2,3,1,4,5])
    can = canonicalize(g, list(range(2, 4)), 0, (baser, gensr, 1, 0))
    assert can == [0,2,1,3,5,4]
    # use a non minimal BSGS
    can = canonicalize(g, list(range(2, 4)), 0, ([2, 0], [Permutation([1,0,2,3,5,4]), Permutation([2,3,0,1,4,5])], 1, 0))
    assert can == [0,2,1,3,5,4]

    """
    The following tests in test_riemann_invariants and in
    test_riemann_invariants1 have been checked using xperm.c from XPerm in
    in [1] and with an older version contained in [2]

    [1] xperm.c part of xPerm written by J. M. Martin-Garcia
        http://www.xact.es/index.html
    [2] test_xperm.cc in cadabra by Kasper Peeters, http://cadabra.phi-sci.com/
    """
    # R_d11^d1_d0^d5 * R^{d6 d4 d0}_d5 * R_{d7 d2 d8 d9} *
    # R_{d10 d3 d6 d4} * R^{d2 d7 d11}_d1 * R^{d8 d9 d3 d10}
    # ord: contravariant d_k ->2*k, covariant d_k -> 2*k+1
    # T_c = R^{d0 d1 d2 d3} * R_{d0 d1}^{d4 d5} * R_{d2 d3}^{d6 d7} *
    # R_{d4 d5}^{d8 d9} * R_{d6 d7}^{d10 d11} * R_{d8 d9 d10 d11}
    g = Permutation([23,2,1,10,12,8,0,11,15,5,17,19,21,7,13,9,4,14,22,3,16,18,6,20,24,25])
    can = canonicalize(g, list(range(24)), 0, (baser, gensr, 6, 0))
    assert can == [0,2,4,6,1,3,8,10,5,7,12,14,9,11,16,18,13,15,20,22,17,19,21,23,24,25]

    # use a non minimal BSGS
    can = canonicalize(g, list(range(24)), 0, ([2, 0], [Permutation([1,0,2,3,5,4]), Permutation([2,3,0,1,4,5])], 6, 0))
    assert can == [0,2,4,6,1,3,8,10,5,7,12,14,9,11,16,18,13,15,20,22,17,19,21,23,24,25]

    g = Permutation([0,2,5,7,4,6,9,11,8,10,13,15,12,14,17,19,16,18,21,23,20,22,25,27,24,26,29,31,28,30,33,35,32,34,37,39,36,38,1,3,40,41])
    can = canonicalize(g, list(range(40)), 0, (baser, gensr, 10, 0))
    assert can == [0,2,4,6,1,3,8,10,5,7,12,14,9,11,16,18,13,15,20,22,17,19,24,26,21,23,28,30,25,27,32,34,29,31,36,38,33,35,37,39,40,41]


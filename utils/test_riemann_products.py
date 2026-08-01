
def test_riemann_products():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    d0, d1, d2, d3, d4, d5, d6 = tensor_indices('d0:7', Lorentz)
    a0, a1, a2, a3, a4, a5 = tensor_indices('a0:6', Lorentz)
    a, b = tensor_indices('a,b', Lorentz)
    R = TensorHead('R', [Lorentz]*4, TensorSymmetry.riemann())
    # R^{a b d0}_d0 = 0
    t = R(a, b, d0, -d0)
    tc = t.canon_bp()
    assert tc == 0

    # R^{d0 b a}_d0
    # T_c = -R^{a d0 b}_d0
    t = R(d0, b, a, -d0)
    tc = t.canon_bp()
    assert str(tc) == '-R(a, L_0, b, -L_0)'

    # R^d1_d2^b_d0 * R^{d0 a}_d1^d2; ord=[a,b,d0,-d0,d1,-d1,d2,-d2]
    # T_c = -R^{a d0 d1 d2}* R^b_{d0 d1 d2}
    t = R(d1, -d2, b, -d0)*R(d0, a, -d1, d2)
    tc = t.canon_bp()
    assert str(tc) == '-R(a, L_0, L_1, L_2)*R(b, -L_0, -L_1, -L_2)'

    # A symmetric commuting
    # R^{d6 d5}_d2^d1 * R^{d4 d0 d2 d3} * A_{d6 d0} A_{d3 d1} * A_{d4 d5}
    # g = [12,10,5,2, 8,0,4,6, 13,1, 7,3, 9,11,14,15]
    # T_c = -R^{d0 d1 d2 d3} * R_d0^{d4 d5 d6} * A_{d1 d4}*A_{d2 d5}*A_{d3 d6}
    V = TensorHead('V', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = R(d6, d5, -d2, d1)*R(d4, d0, d2, d3)*V(-d6, -d0)*V(-d3, -d1)*V(-d4, -d5)
    tc = t.canon_bp()
    assert str(tc) == '-R(L_0, L_1, L_2, L_3)*R(-L_0, L_4, L_5, L_6)*V(-L_1, -L_4)*V(-L_2, -L_5)*V(-L_3, -L_6)'

    # R^{d2 a0 a2 d0} * R^d1_d2^{a1 a3} * R^{a4 a5}_{d0 d1}
    # T_c = R^{a0 d0 a2 d1}*R^{a1 a3}_d0^d2*R^{a4 a5}_{d1 d2}
    t = R(d2, a0, a2, d0)*R(d1, -d2, a1, a3)*R(a4, a5, -d0, -d1)
    tc = t.canon_bp()
    assert str(tc) == 'R(a0, L_0, a2, L_1)*R(a1, a3, -L_0, L_2)*R(a4, a5, -L_1, -L_2)'


def test_riemann_products():
    baser, gensr = riemann_bsgs
    base1, gens1 = get_symmetric_group_sgs(1)
    base2, gens2 = get_symmetric_group_sgs(2)
    base2a, gens2a = get_symmetric_group_sgs(2, 1)

    # R^{a b d0}_d0 = 0
    g = Permutation([0,1,2,3,4,5])
    can = canonicalize(g, list(range(2,4)), 0, (baser, gensr, 1, 0))
    assert can == 0

    # R^{d0 b a}_d0 ; ord = [a,b,d0,-d0}; g = [2,1,0,3,4,5]
    # T_c = -R^{a d0 b}_d0;  can = [0,2,1,3,5,4]
    g = Permutation([2,1,0,3,4,5])
    can = canonicalize(g, list(range(2, 4)), 0, (baser, gensr, 1, 0))
    assert can == [0,2,1,3,5,4]

    # R^d1_d2^b_d0 * R^{d0 a}_d1^d2; ord=[a,b,d0,-d0,d1,-d1,d2,-d2]
    # g = [4,7,1,3,2,0,5,6,8,9]
    # T_c = -R^{a d0 d1 d2}* R^b_{d0 d1 d2}
    # can = [0,2,4,6,1,3,5,7,9,8]
    g = Permutation([4,7,1,3,2,0,5,6,8,9])
    can = canonicalize(g, list(range(2,8)), 0, (baser, gensr, 2, 0))
    assert can == [0,2,4,6,1,3,5,7,9,8]
    can1 = canonicalize_naive(g, list(range(2,8)), 0, (baser, gensr, 2, 0))
    assert can == can1

    # A symmetric commuting
    # R^{d6 d5}_d2^d1 * R^{d4 d0 d2 d3} * A_{d6 d0} A_{d3 d1} * A_{d4 d5}
    # g = [12,10,5,2, 8,0,4,6, 13,1, 7,3, 9,11,14,15]
    # T_c = -R^{d0 d1 d2 d3} * R_d0^{d4 d5 d6} * A_{d1 d4}*A_{d2 d5}*A_{d3 d6}

    g = Permutation([12,10,5,2,8,0,4,6,13,1,7,3,9,11,14,15])
    can = canonicalize(g, list(range(14)), 0, ((baser,gensr,2,0)), (base2,gens2,3,0))
    assert can == [0, 2, 4, 6, 1, 8, 10, 12, 3, 9, 5, 11, 7, 13, 15, 14]

    # R^{d2 a0 a2 d0} * R^d1_d2^{a1 a3} * R^{a4 a5}_{d0 d1}
    # ord = [a0,a1,a2,a3,a4,a5,d0,-d0,d1,-d1,d2,-d2]
    #         0  1  2  3 4  5  6   7  8   9  10  11
    # can = [0, 6, 2, 8, 1, 3, 7, 10, 4, 5, 9, 11, 12, 13]
    # T_c = R^{a0 d0 a2 d1}*R^{a1 a3}_d0^d2*R^{a4 a5}_{d1 d2}
    g = Permutation([10,0,2,6,8,11,1,3,4,5,7,9,12,13])
    can = canonicalize(g, list(range(6,12)), 0, (baser, gensr, 3, 0))
    assert can == [0, 6, 2, 8, 1, 3, 7, 10, 4, 5, 9, 11, 12, 13]
    #can1 = canonicalize_naive(g, list(range(6,12)), 0, (baser, gensr, 3, 0))
    #assert can == can1

    # A^n_{i, j} antisymmetric in i,j
    # A_m0^d0_a1 * A_m1^a0_d0; ord = [m0,m1,a0,a1,d0,-d0]
    # g = [0,4,3,1,2,5,6,7]
    # T_c = -A_{m a1}^d0 * A_m1^a0_d0
    # can = [0,3,4,1,2,5,7,6]
    base, gens = bsgs_direct_product(base1, gens1, base2a, gens2a)
    dummies = list(range(4, 6))
    g = Permutation([0,4,3,1,2,5,6,7])
    can = canonicalize(g, dummies, 0, (base, gens, 2, 0))
    assert can == [0, 3, 4, 1, 2, 5, 7, 6]


    # A^n_{i, j} symmetric in i,j
    # A^m0_a0^d2 * A^n0_d2^d1 * A^n1_d1^d0 * A_{m0 d0}^a1
    # ordering: first the free indices; then first n, then d
    # ord=[n0,n1,a0,a1, m0,-m0,d0,-d0,d1,-d1,d2,-d2]
    #      0  1   2  3   4  5  6   7  8   9  10  11]
    # g = [4,2,10, 0,11,8, 1,9,6, 5,7,3, 12,13]
    # if the dummy indices m_i and d_i were separated,
    # one gets
    # T_c = A^{n0 d0 d1} * A^n1_d0^d2 * A^m0^a0_d1 * A_m0^a1_d2
    # can = [0, 6, 8, 1, 7, 10, 4, 2, 9, 5, 3, 11, 12, 13]
    # If they are not, so can is
    # T_c = A^{n0 m0 d0} A^n1_m0^d1 A^{d2 a0}_d0 A_d2^a1_d1
    # can = [0, 4, 6, 1, 5, 8, 10, 2, 7, 11, 3, 9, 12, 13]
    # case with single type of indices

    base, gens = bsgs_direct_product(base1, gens1, base2, gens2)
    dummies = list(range(4, 12))
    g = Permutation([4,2,10, 0,11,8, 1,9,6, 5,7,3, 12,13])
    can = canonicalize(g, dummies, 0, (base, gens, 4, 0))
    assert can == [0, 4, 6, 1, 5, 8, 10, 2, 7, 11, 3, 9, 12, 13]
    # case with separated indices
    dummies = [list(range(4, 6)), list(range(6,12))]
    sym = [0, 0]
    can = canonicalize(g, dummies, sym, (base, gens, 4, 0))
    assert can == [0, 6, 8, 1, 7, 10, 4, 2, 9, 5, 3, 11, 12, 13]
    # case with separated indices with the second type of index
    # with antisymmetric metric: there is a sign change
    sym = [0, 1]
    can = canonicalize(g, dummies, sym, (base, gens, 4, 0))
    assert can == [0, 6, 8, 1, 7, 10, 4, 2, 9, 5, 3, 11, 13, 12]


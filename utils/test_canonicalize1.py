
def test_canonicalize1():
    Lorentz = TensorIndexType('Lorentz', dummy_name='L')
    a, a0, a1, a2, a3, b, d0, d1, d2, d3 = \
        tensor_indices('a,a0,a1,a2,a3,b,d0,d1,d2,d3', Lorentz)

    # A_d0*A^d0; ord = [d0,-d0]
    # T_c = A^d0*A_d0
    A = TensorHead('A', [Lorentz], TensorSymmetry.no_symmetry(1))
    t = A(-d0)*A(d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0)*A(-L_0)'

    # A commuting
    # A_d0*A_d1*A_d2*A^d2*A^d1*A^d0
    # T_c = A^d0*A_d0*A^d1*A_d1*A^d2*A_d2
    t = A(-d0)*A(-d1)*A(-d2)*A(d2)*A(d1)*A(d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0)*A(-L_0)*A(L_1)*A(-L_1)*A(L_2)*A(-L_2)'

    # A anticommuting
    # A_d0*A_d1*A_d2*A^d2*A^d1*A^d0
    # T_c 0
    A = TensorHead('A', [Lorentz], TensorSymmetry.no_symmetry(1), 1)
    t = A(-d0)*A(-d1)*A(-d2)*A(d2)*A(d1)*A(d0)
    tc = t.canon_bp()
    assert tc == 0

    # A commuting symmetric
    # A^{d0 b}*A^a_d1*A^d1_d0
    # T_c = A^{a d0}*A^{b d1}*A_{d0 d1}
    A = TensorHead('A', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(d0, b)*A(a, -d1)*A(d1, -d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(a, L_0)*A(b, L_1)*A(-L_0, -L_1)'

    # A, B commuting symmetric
    # A^{d0 b}*A^d1_d0*B^a_d1
    # T_c = A^{b d0}*A_d0^d1*B^a_d1
    B = TensorHead('B', [Lorentz]*2, TensorSymmetry.fully_symmetric(2))
    t = A(d0, b)*A(d1, -d0)*B(a, -d1)
    tc = t.canon_bp()
    assert str(tc) == 'A(b, L_0)*A(-L_0, L_1)*B(a, -L_1)'

    # A commuting symmetric
    # A^{d1 d0 b}*A^{a}_{d1 d0}; ord=[a,b, d0,-d0,d1,-d1]
    # T_c = A^{a d0 d1}*A^{b}_{d0 d1}
    A = TensorHead('A', [Lorentz]*3, TensorSymmetry.fully_symmetric(3))
    t = A(d1, d0, b)*A(a, -d1, -d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(a, L_0, L_1)*A(b, -L_0, -L_1)'

    # A^{d3 d0 d2}*A^a0_{d1 d2}*A^d1_d3^a1*A^{a2 a3}_d0
    # T_c = A^{a0 d0 d1}*A^a1_d0^d2*A^{a2 a3 d3}*A_{d1 d2 d3}
    t = A(d3, d0, d2)*A(a0, -d1, -d2)*A(d1, -d3, a1)*A(a2, a3, -d0)
    tc = t.canon_bp()
    assert str(tc) == 'A(a0, L_0, L_1)*A(a1, -L_0, L_2)*A(a2, a3, L_3)*A(-L_1, -L_2, -L_3)'

    # A commuting symmetric, B antisymmetric
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # in this esxample and in the next three,
    # renaming dummy indices and using symmetry of A,
    # T = A^{d0 d1 d2} * A_{d0 d1 d3} * B_d2^d3
    # can = 0
    A = TensorHead('A', [Lorentz]*3, TensorSymmetry.fully_symmetric(3))
    B = TensorHead('B', [Lorentz]*2, TensorSymmetry.fully_symmetric(-2))
    t = A(d0, d1, d2)*A(-d2, -d3, -d1)*B(-d0, d3)
    tc = t.canon_bp()
    assert tc == 0

    # A anticommuting symmetric, B antisymmetric
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # T_c = A^{d0 d1 d2} * A_{d0 d1}^d3 * B_{d2 d3}
    A = TensorHead('A', [Lorentz]*3, TensorSymmetry.fully_symmetric(3), 1)
    B = TensorHead('B', [Lorentz]*2, TensorSymmetry.fully_symmetric(-2))
    t = A(d0, d1, d2)*A(-d2, -d3, -d1)*B(-d0, d3)
    tc = t.canon_bp()
    assert str(tc) == 'A(L_0, L_1, L_2)*A(-L_0, -L_1, L_3)*B(-L_2, -L_3)'

    # A anticommuting symmetric, B antisymmetric commuting, antisymmetric metric
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # T_c = -A^{d0 d1 d2} * A_{d0 d1}^d3 * B_{d2 d3}
    Spinor = TensorIndexType('Spinor', dummy_name='S', metric_symmetry=-1)
    a, a0, a1, a2, a3, b, d0, d1, d2, d3 = \
        tensor_indices('a,a0,a1,a2,a3,b,d0,d1,d2,d3', Spinor)
    A = TensorHead('A', [Spinor]*3, TensorSymmetry.fully_symmetric(3), 1)
    B = TensorHead('B', [Spinor]*2, TensorSymmetry.fully_symmetric(-2))
    t = A(d0, d1, d2)*A(-d2, -d3, -d1)*B(-d0, d3)
    tc = t.canon_bp()
    assert str(tc) == '-A(S_0, S_1, S_2)*A(-S_0, -S_1, S_3)*B(-S_2, -S_3)'

    # A anticommuting symmetric, B antisymmetric anticommuting,
    # no metric symmetry
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # T_c = A^{d0 d1 d2} * A_{d0 d1 d3} * B_d2^d3
    Mat = TensorIndexType('Mat', metric_symmetry=0, dummy_name='M')
    a, a0, a1, a2, a3, b, d0, d1, d2, d3 = \
        tensor_indices('a,a0,a1,a2,a3,b,d0,d1,d2,d3', Mat)
    A = TensorHead('A', [Mat]*3, TensorSymmetry.fully_symmetric(3), 1)
    B = TensorHead('B', [Mat]*2, TensorSymmetry.fully_symmetric(-2))
    t = A(d0, d1, d2)*A(-d2, -d3, -d1)*B(-d0, d3)
    tc = t.canon_bp()
    assert str(tc) == 'A(M_0, M_1, M_2)*A(-M_0, -M_1, -M_3)*B(-M_2, M_3)'

    # Gamma anticommuting
    # Gamma_{mu nu} * gamma^rho * Gamma^{nu mu alpha}
    # T_c = -Gamma^{mu nu} * gamma^rho * Gamma_{alpha mu nu}
    alpha, beta, gamma, mu, nu, rho = \
        tensor_indices('alpha,beta,gamma,mu,nu,rho', Lorentz)
    Gamma = TensorHead('Gamma', [Lorentz],
                       TensorSymmetry.fully_symmetric(1), 2)
    Gamma2 = TensorHead('Gamma', [Lorentz]*2,
                        TensorSymmetry.fully_symmetric(-2), 2)
    Gamma3 = TensorHead('Gamma', [Lorentz]*3,
                        TensorSymmetry.fully_symmetric(-3), 2)
    t = Gamma2(-mu, -nu)*Gamma(rho)*Gamma3(nu, mu, alpha)
    tc = t.canon_bp()
    assert str(tc) == '-Gamma(L_0, L_1)*Gamma(rho)*Gamma(alpha, -L_0, -L_1)'

    # Gamma_{mu nu} * Gamma^{gamma beta} * gamma_rho * Gamma^{nu mu alpha}
    # T_c = Gamma^{mu nu} * Gamma^{beta gamma} * gamma_rho * Gamma^alpha_{mu nu}
    t = Gamma2(mu, nu)*Gamma2(beta, gamma)*Gamma(-rho)*Gamma3(alpha, -mu, -nu)
    tc = t.canon_bp()
    assert str(tc) == 'Gamma(L_0, L_1)*Gamma(beta, gamma)*Gamma(-rho)*Gamma(alpha, -L_0, -L_1)'

    # f^a_{b,c} antisymmetric in b,c; A_mu^a no symmetry
    # f^c_{d a} * f_{c e b} * A_mu^d * A_nu^a * A^{nu e} * A^{mu b}
    # g = [8,11,5, 9,13,7, 1,10, 3,4, 2,12, 0,6, 14,15]
    # T_c = -f^{a b c} * f_a^{d e} * A^mu_b * A_{mu d} * A^nu_c * A_{nu e}
    Flavor = TensorIndexType('Flavor', dummy_name='F')
    a, b, c, d, e, ff = tensor_indices('a,b,c,d,e,f', Flavor)
    mu, nu = tensor_indices('mu,nu', Lorentz)
    f = TensorHead('f', [Flavor]*3, TensorSymmetry.direct_product(1, -2))
    A = TensorHead('A', [Lorentz, Flavor], TensorSymmetry.no_symmetry(2))
    t = f(c, -d, -a)*f(-c, -e, -b)*A(-mu, d)*A(-nu, a)*A(nu, e)*A(mu, b)
    tc = t.canon_bp()
    assert str(tc) == '-f(F_0, F_1, F_2)*f(-F_0, F_3, F_4)*A(L_0, -F_1)*A(-L_0, -F_3)*A(L_1, -F_2)*A(-L_1, -F_4)'


def test_canonicalize1():
    base1, gens1 = get_symmetric_group_sgs(1)
    base1a, gens1a = get_symmetric_group_sgs(1, 1)
    base2, gens2 = get_symmetric_group_sgs(2)
    base3, gens3 = get_symmetric_group_sgs(3)
    base2a, gens2a = get_symmetric_group_sgs(2, 1)
    base3a, gens3a = get_symmetric_group_sgs(3, 1)

    # A_d0*A^d0; ord = [d0,-d0]; g = [1,0,2,3]
    # T_c = A^d0*A_d0; can = [0,1,2,3]
    g = Permutation([1,0,2,3])
    can = canonicalize(g, [0, 1], 0, (base1, gens1, 2, 0))
    assert can == list(range(4))

    # A commuting
    # A_d0*A_d1*A_d2*A^d2*A^d1*A^d0; ord=[d0,-d0,d1,-d1,d2,-d2]
    # g = [1,3,5,4,2,0,6,7]
    # T_c = A^d0*A_d0*A^d1*A_d1*A^d2*A_d2; can = list(range(8))
    g = Permutation([1,3,5,4,2,0,6,7])
    can = canonicalize(g, list(range(6)), 0, (base1, gens1, 6, 0))
    assert can == list(range(8))

    # A anticommuting
    # A_d0*A_d1*A_d2*A^d2*A^d1*A^d0; ord=[d0,-d0,d1,-d1,d2,-d2]
    # g = [1,3,5,4,2,0,6,7]
    # T_c 0;  can = 0
    g = Permutation([1,3,5,4,2,0,6,7])
    can = canonicalize(g, list(range(6)), 0, (base1, gens1, 6, 1))
    assert can == 0
    can1 = canonicalize_naive(g, list(range(6)), 0, (base1, gens1, 6, 1))
    assert can1 == 0

    # A commuting symmetric
    # A^{d0 b}*A^a_d1*A^d1_d0; ord=[a,b,d0,-d0,d1,-d1]
    # g = [2,1,0,5,4,3,6,7]
    # T_c = A^{a d0}*A^{b d1}*A_{d0 d1}; can = [0,2,1,4,3,5,6,7]
    g = Permutation([2,1,0,5,4,3,6,7])
    can = canonicalize(g, list(range(2,6)), 0, (base2, gens2, 3, 0))
    assert can == [0,2,1,4,3,5,6,7]

    # A, B commuting symmetric
    # A^{d0 b}*A^d1_d0*B^a_d1; ord=[a,b,d0,-d0,d1,-d1]
    # g = [2,1,4,3,0,5,6,7]
    # T_c = A^{b d0}*A_d0^d1*B^a_d1; can = [1,2,3,4,0,5,6,7]
    g = Permutation([2,1,4,3,0,5,6,7])
    can = canonicalize(g, list(range(2,6)), 0, (base2,gens2,2,0), (base2,gens2,1,0))
    assert can == [1,2,3,4,0,5,6,7]

    # A commuting symmetric
    # A^{d1 d0 b}*A^{a}_{d1 d0}; ord=[a,b, d0,-d0,d1,-d1]
    # g = [4,2,1,0,5,3,6,7]
    # T_c = A^{a d0 d1}*A^{b}_{d0 d1}; can = [0,2,4,1,3,5,6,7]
    g = Permutation([4,2,1,0,5,3,6,7])
    can = canonicalize(g, list(range(2,6)), 0, (base3, gens3, 2, 0))
    assert can == [0,2,4,1,3,5,6,7]


    # A^{d3 d0 d2}*A^a0_{d1 d2}*A^d1_d3^a1*A^{a2 a3}_d0
    # ord = [a0,a1,a2,a3,d0,-d0,d1,-d1,d2,-d2,d3,-d3]
    #        0   1  2  3  4  5  6   7  8   9  10  11
    # g = [10,4,8, 0,7,9, 6,11,1, 2,3,5, 12,13]
    # T_c = A^{a0 d0 d1}*A^a1_d0^d2*A^{a2 a3 d3}*A_{d1 d2 d3}
    # can = [0,4,6, 1,5,8, 2,3,10, 7,9,11, 12,13]
    g = Permutation([10,4,8, 0,7,9, 6,11,1, 2,3,5, 12,13])
    can = canonicalize(g, list(range(4,12)), 0, (base3, gens3, 4, 0))
    assert can == [0,4,6, 1,5,8, 2,3,10, 7,9,11, 12,13]

    # A commuting symmetric, B antisymmetric
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # ord = [d0,-d0,d1,-d1,d2,-d2,d3,-d3]
    # g = [0,2,4,5,7,3,1,6,8,9]
    # in this esxample and in the next three,
    # renaming dummy indices and using symmetry of A,
    # T = A^{d0 d1 d2} * A_{d0 d1 d3} * B_d2^d3
    # can = 0
    g = Permutation([0,2,4,5,7,3,1,6,8,9])
    can = canonicalize(g, list(range(8)), 0, (base3, gens3,2,0), (base2a,gens2a,1,0))
    assert can == 0
    # A anticommuting symmetric, B anticommuting
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # T_c = A^{d0 d1 d2} * A_{d0 d1}^d3 * B_{d2 d3}
    # can = [0,2,4, 1,3,6, 5,7, 8,9]
    can = canonicalize(g, list(range(8)), 0, (base3, gens3,2,1), (base2a,gens2a,1,0))
    assert can == [0,2,4, 1,3,6, 5,7, 8,9]
    # A anticommuting symmetric, B antisymmetric commuting, antisymmetric metric
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # T_c = -A^{d0 d1 d2} * A_{d0 d1}^d3 * B_{d2 d3}
    # can = [0,2,4, 1,3,6, 5,7, 9,8]
    can = canonicalize(g, list(range(8)), 1, (base3, gens3,2,1), (base2a,gens2a,1,0))
    assert can == [0,2,4, 1,3,6, 5,7, 9,8]

    # A anticommuting symmetric, B anticommuting anticommuting,
    # no metric symmetry
    # A^{d0 d1 d2} * A_{d2 d3 d1} * B_d0^d3
    # T_c = A^{d0 d1 d2} * A_{d0 d1 d3} * B_d2^d3
    # can = [0,2,4, 1,3,7, 5,6, 8,9]
    can = canonicalize(g, list(range(8)), None, (base3, gens3,2,1), (base2a,gens2a,1,0))
    assert can == [0,2,4,1,3,7,5,6,8,9]

    # Gamma anticommuting
    # Gamma_{mu nu} * gamma^rho * Gamma^{nu mu alpha}
    # ord = [alpha, rho, mu,-mu,nu,-nu]
    # g = [3,5,1,4,2,0,6,7]
    # T_c = -Gamma^{mu nu} * gamma^rho * Gamma_{alpha mu nu}
    # can = [2,4,1,0,3,5,7,6]]
    g = Permutation([3,5,1,4,2,0,6,7])
    t0 = (base2a, gens2a, 1, None)
    t1 = (base1, gens1, 1, None)
    t2 = (base3a, gens3a, 1, None)
    can = canonicalize(g, list(range(2, 6)), 0, t0, t1, t2)
    assert can == [2,4,1,0,3,5,7,6]

    # Gamma_{mu nu} * Gamma^{gamma beta} * gamma_rho * Gamma^{nu mu alpha}
    # ord = [alpha, beta, gamma, -rho, mu,-mu,nu,-nu]
    #         0      1      2     3    4   5   6  7
    # g = [5,7,2,1,3,6,4,0,8,9]
    # T_c = Gamma^{mu nu} * Gamma^{beta gamma} * gamma_rho * Gamma^alpha_{mu nu}    # can = [4,6,1,2,3,0,5,7,8,9]
    t0 = (base2a, gens2a, 2, None)
    g = Permutation([5,7,2,1,3,6,4,0,8,9])
    can = canonicalize(g, list(range(4, 8)), 0, t0, t1, t2)
    assert can == [4,6,1,2,3,0,5,7,8,9]

    # f^a_{b,c} antisymmetric in b,c; A_mu^a no symmetry
    # f^c_{d a} * f_{c e b} * A_mu^d * A_nu^a * A^{nu e} * A^{mu b}
    # ord = [mu,-mu,nu,-nu,a,-a,b,-b,c,-c,d,-d, e, -e]
    #         0  1  2   3  4  5 6  7 8  9 10 11 12 13
    # g = [8,11,5, 9,13,7, 1,10, 3,4, 2,12, 0,6, 14,15]
    # T_c = -f^{a b c} * f_a^{d e} * A^mu_b * A_{mu d} * A^nu_c * A_{nu e}
    # can = [4,6,8,       5,10,12,   0,7,     1,11,       2,9,    3,13, 15,14]
    g = Permutation([8,11,5, 9,13,7, 1,10, 3,4, 2,12, 0,6, 14,15])
    base_f, gens_f = bsgs_direct_product(base1, gens1, base2a, gens2a)
    base_A, gens_A = bsgs_direct_product(base1, gens1, base1, gens1)
    t0 = (base_f, gens_f, 2, 0)
    t1 = (base_A, gens_A, 4, 0)
    can = canonicalize(g, [list(range(4)), list(range(4, 14))], [0, 0], t0, t1)
    assert can == [4,6,8, 5,10,12, 0,7, 1,11, 2,9, 3,13, 15,14]


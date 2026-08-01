
def test_substitution_with_infeasible_solution():
    a00, a01, a10, a11, l0, l1, l2, l3, m0, m1, m2, m3, m4, m5, m6, m7, c00, c01, c10, c11, p00, p01, p10, p11 = symbols(
        'a00, a01, a10, a11, l0, l1, l2, l3, m0, m1, m2, m3, m4, m5, m6, m7, c00, c01, c10, c11, p00, p01, p10, p11'
    )
    solvefor = [p00, p01, p10, p11, c00, c01, c10, c11, m0, m1, m3, l0, l1, l2, l3]
    system = [
        -l0 * c00 - l1 * c01 + m0 + c00 + c01,
        -l0 * c10 - l1 * c11 + m1,
        -l2 * c00 - l3 * c01 + c00 + c01,
        -l2 * c10 - l3 * c11 + m3,
        -l0 * p00 - l2 * p10 + p00 + p10,
        -l1 * p00 - l3 * p10 + p00 + p10,
        -l0 * p01 - l2 * p11,
        -l1 * p01 - l3 * p11,
        -a00 + c00 * p00 + c10 * p01,
        -a01 + c01 * p00 + c11 * p01,
        -a10 + c00 * p10 + c10 * p11,
        -a11 + c01 * p10 + c11 * p11,
        -m0 * p00,
        -m1 * p01,
        -m2 * p10,
        -m3 * p11,
        -m4 * c00,
        -m5 * c01,
        -m6 * c10,
        -m7 * c11,
        m2,
        m4,
        m5,
        m6,
        m7
    ]
    sol = FiniteSet(
        (0, Complement(FiniteSet(p01), FiniteSet(0)), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, l2, l3),
        (p00, Complement(FiniteSet(p01), FiniteSet(0)), 0, p11, 0, 0, 0, 0, 0, 0, 0, 1, 1, -p01/p11, -p01/p11),
        (0, Complement(FiniteSet(p01), FiniteSet(0)), 0, p11, 0, 0, 0, 0, 0, 0, 0, 1, -l3*p11/p01, -p01/p11, l3),
        (0, Complement(FiniteSet(p01), FiniteSet(0)), 0, p11, 0, 0, 0, 0, 0, 0, 0, -l2*p11/p01, -l3*p11/p01, l2, l3),
    )
    assert sol != nonlinsolve(system, solvefor)


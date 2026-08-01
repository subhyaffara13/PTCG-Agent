
def test_solve_for_ild_reactions():
    E = Symbol('E')
    I = Symbol('I')
    b = Beam(10, E, I)
    b.apply_support(0, type="pin")
    b.apply_support(10, type="pin")
    R_0, R_10 = symbols('R_0, R_10')
    b.solve_for_ild_reactions(1, R_0, R_10)
    a = b.ild_variable
    assert b.ild_reactions == {R_0: -SingularityFunction(a, 0, 0) + SingularityFunction(a, 0, 1)/10
                                    - SingularityFunction(a, 10, 1)/10,
                               R_10: -SingularityFunction(a, 0, 1)/10 + SingularityFunction(a, 10, 0)
                                     + SingularityFunction(a, 10, 1)/10}

    E = Symbol('E')
    I = Symbol('I')
    F = Symbol('F')
    L = Symbol('L', positive=True)
    b = Beam(L, E, I)
    b.apply_support(L, type="fixed")
    b.apply_load(F, 0, -1)
    R_L, M_L = symbols('R_L, M_L')
    b.solve_for_ild_reactions(F, R_L, M_L)
    a = b.ild_variable
    assert b.ild_reactions == {R_L: -F*SingularityFunction(a, 0, 0) + F*SingularityFunction(a, L, 0) - F,
                               M_L: -F*L*SingularityFunction(a, 0, 0) - F*L + F*SingularityFunction(a, 0, 1)
                                    - F*SingularityFunction(a, L, 1)}

    E = Symbol('E')
    I = Symbol('I')
    b = Beam(20, E, I)
    r0 = b.apply_support(0, type="pin")
    r5 = b.apply_support(5, type="pin")
    r10 = b.apply_support(10, type="pin")
    r20, m20 = b.apply_support(20, type="fixed")
    b.solve_for_ild_reactions(1, r0, r5, r10, r20, m20)
    a = b.ild_variable
    assert b.ild_reactions[r0].subs(a, 4) == -Rational(59, 475)
    assert b.ild_reactions[r5].subs(a, 4) == -Rational(2296, 2375)
    assert b.ild_reactions[r10].subs(a, 4) == Rational(243, 2375)
    assert b.ild_reactions[r20].subs(a, 12) == -Rational(83, 475)
    assert b.ild_reactions[m20].subs(a, 12) == -Rational(264, 475)


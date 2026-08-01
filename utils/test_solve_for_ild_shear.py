
def test_solve_for_ild_shear():
    E = Symbol('E')
    I = Symbol('I')
    F = Symbol('F')
    L1 = Symbol('L1', positive=True)
    L2 = Symbol('L2', positive=True)
    b = Beam(L1 + L2, E, I)
    r0 = b.apply_support(0, type="pin")
    rL = b.apply_support(L1 + L2, type="pin")
    b.solve_for_ild_reactions(F, r0, rL)
    b.solve_for_ild_shear(L1, F, r0, rL)
    a = b.ild_variable
    expected_shear = (-F*L1*SingularityFunction(a, 0, 0)/(L1 + L2) - F*L2*SingularityFunction(a, 0, 0)/(L1 + L2)
                      - F*SingularityFunction(-a, 0, 0) + F*SingularityFunction(a, L1 + L2, 0) + F
                      + F*SingularityFunction(a, 0, 1)/(L1 + L2) - F*SingularityFunction(a, L1 + L2, 1)/(L1 + L2)
                      - (-F*L1*SingularityFunction(a, 0, 0)/(L1 + L2) + F*L1*SingularityFunction(a, L1 + L2, 0)/(L1 + L2)
                         - F*L2*SingularityFunction(a, 0, 0)/(L1 + L2) + F*L2*SingularityFunction(a, L1 + L2, 0)/(L1 + L2)
                         + 2*F)*SingularityFunction(a, L1, 0))
    assert b.ild_shear.expand() == expected_shear.expand()

    E = Symbol('E')
    I = Symbol('I')
    b = Beam(20, E, I)
    r0 = b.apply_support(0, type="pin")
    r5 = b.apply_support(5, type="pin")
    r10 = b.apply_support(10, type="pin")
    r20, m20 = b.apply_support(20, type="fixed")
    b.solve_for_ild_reactions(1, r0, r5, r10, r20, m20)
    b.solve_for_ild_shear(6, 1, r0, r5, r10, r20, m20)
    a = b.ild_variable
    assert b.ild_shear.subs(a, 12) == Rational(96, 475)
    assert b.ild_shear.subs(a, 4) == -Rational(216, 2375)


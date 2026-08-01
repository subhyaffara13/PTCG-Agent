
def test_solve_for_ild_moment():
    E = Symbol('E')
    I = Symbol('I')
    F = Symbol('F')
    L1 = Symbol('L1', positive=True)
    L2 = Symbol('L2', positive=True)
    b = Beam(L1 + L2, E, I)
    r0 = b.apply_support(0, type="pin")
    rL = b.apply_support(L1 + L2, type="pin")
    a = b.ild_variable
    b.solve_for_ild_reactions(F, r0, rL)
    b.solve_for_ild_moment(L1, F, r0, rL)
    assert b.ild_moment.subs(a, 3).subs(L1, 5).subs(L2, 5) == -3*F/2

    E = Symbol('E')
    I = Symbol('I')
    b = Beam(20, E, I)
    r0 = b.apply_support(0, type="pin")
    r5 = b.apply_support(5, type="pin")
    r10 = b.apply_support(10, type="pin")
    r20, m20 = b.apply_support(20, type="fixed")
    b.solve_for_ild_reactions(1, r0, r5, r10, r20, m20)
    b.solve_for_ild_moment(5, 1, r0, r5, r10, r20, m20)
    assert b.ild_moment.subs(a, 12) == -Rational(96, 475)
    assert b.ild_moment.subs(a, 4) == Rational(36, 95)


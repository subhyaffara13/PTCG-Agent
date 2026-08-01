
def test_apply_support():
    E = Symbol('E')
    I = Symbol('I')

    b = Beam(4, E, I)
    b.apply_support(0, "cantilever")
    b.apply_load(20, 4, -1)
    M_0, R_0 = symbols('M_0, R_0')
    b.solve_for_reaction_loads(R_0, M_0)
    assert simplify(b.slope()) == simplify((80*SingularityFunction(x, 0, 1) - 10*SingularityFunction(x, 0, 2)
                + 10*SingularityFunction(x, 4, 2))/(E*I))
    assert simplify(b.deflection()) == simplify((40*SingularityFunction(x, 0, 2) - 10*SingularityFunction(x, 0, 3)/3
                + 10*SingularityFunction(x, 4, 3)/3)/(E*I))

    b = Beam(30, E, I)
    p0 = b.apply_support(10, "pin")
    p1 = b.apply_support(30, "roller")
    b.apply_load(-8, 0, -1)
    b.apply_load(120, 30, -2)
    b.solve_for_reaction_loads(p0, p1)
    assert b.slope() == (-4*SingularityFunction(x, 0, 2) + 3*SingularityFunction(x, 10, 2)
            + 120*SingularityFunction(x, 30, 1) + SingularityFunction(x, 30, 2) + Rational(4000, 3))/(E*I)
    assert b.deflection() == (x*Rational(4000, 3) - 4*SingularityFunction(x, 0, 3)/3 + SingularityFunction(x, 10, 3)
            + 60*SingularityFunction(x, 30, 2) + SingularityFunction(x, 30, 3)/3 - 12000)/(E*I)
    R_10 = Symbol('R_10')
    R_30 = Symbol('R_30')
    assert p0 == R_10
    assert b.reaction_loads == {R_10: 6, R_30: 2}
    assert b.reaction_loads[p0] == 6

    b = Beam(8, E, I)
    p0, m0 = b.apply_support(0, "fixed")
    p1 = b.apply_support(8, "roller")
    b.apply_load(-5, 0, 0, 8)
    b.solve_for_reaction_loads(p0, m0, p1)
    R_0 = Symbol('R_0')
    M_0 = Symbol('M_0')
    R_8 = Symbol('R_8')
    assert p0 == R_0
    assert m0 == M_0
    assert p1 == R_8
    assert b.reaction_loads == {R_0: 25, M_0: -40, R_8: 15}
    assert b.reaction_loads[m0] == -40

    P = Symbol('P', positive=True)
    L = Symbol('L', positive=True)
    b = Beam(L, E, I)
    b.apply_support(0, type='fixed')
    b.apply_support(L, type='fixed')
    b.apply_load(-P, L/2, -1)
    R_0, R_L, M_0, M_L = symbols('R_0, R_L, M_0, M_L')
    b.solve_for_reaction_loads(R_0, R_L, M_0, M_L)
    assert b.reaction_loads == {R_0: P/2, R_L: P/2, M_0: -L*P/8, M_L: L*P/8}



def test_composite_beam():
    E = Symbol('E')
    I = Symbol('I')
    b1 = Beam(2, E, 1.5*I)
    b2 = Beam(2, E, I)
    b = b1.join(b2, "fixed")
    b.apply_load(-20, 0, -1)
    b.apply_load(80, 0, -2)
    b.apply_load(20, 4, -1)
    b.bc_slope = [(0, 0)]
    b.bc_deflection = [(0, 0)]
    assert b.length == 4
    assert b.second_moment == Piecewise((1.5*I, x <= 2), (I, x <= 4))
    assert b.slope().subs(x, 4) == 120.0/(E*I)
    assert b.slope().subs(x, 2) == 80.0/(E*I)
    assert int(b.deflection().subs(x, 4).args[0]) == -302  # Coefficient of 1/(E*I)

    l = symbols('l', positive=True)
    R1, M1, R2, R3, P = symbols('R1 M1 R2 R3 P')
    b1 = Beam(2*l, E, I)
    b2 = Beam(2*l, E, I)
    b = b1.join(b2,"hinge")
    b.apply_load(M1, 0, -2)
    b.apply_load(R1, 0, -1)
    b.apply_load(R2, l, -1)
    b.apply_load(R3, 4*l, -1)
    b.apply_load(P, 3*l, -1)
    b.bc_slope = [(0, 0)]
    b.bc_deflection = [(0, 0), (l, 0), (4*l, 0)]
    b.solve_for_reaction_loads(M1, R1, R2, R3)
    assert b.reaction_loads == {R3: -P/2, R2: P*Rational(-5, 4), M1: -P*l/4, R1: P*Rational(3, 4)}
    assert b.slope().subs(x, 3*l) == -7*P*l**2/(48*E*I)
    assert b.deflection().subs(x, 2*l) == 7*P*l**3/(24*E*I)
    assert b.deflection().subs(x, 3*l) == 5*P*l**3/(16*E*I)

    # When beams having same second moment are joined.
    b1 = Beam(2, 500, 10)
    b2 = Beam(2, 500, 10)
    b = b1.join(b2, "fixed")
    b.apply_load(M1, 0, -2)
    b.apply_load(R1, 0, -1)
    b.apply_load(R2, 1, -1)
    b.apply_load(R3, 4, -1)
    b.apply_load(10, 3, -1)
    b.bc_slope = [(0, 0)]
    b.bc_deflection = [(0, 0), (1, 0), (4, 0)]
    b.solve_for_reaction_loads(M1, R1, R2, R3)
    assert b.slope() == -2*SingularityFunction(x, 0, 1)/5625 + SingularityFunction(x, 0, 2)/1875\
                - 133*SingularityFunction(x, 1, 2)/135000 + SingularityFunction(x, 3, 2)/1000\
                - 37*SingularityFunction(x, 4, 2)/67500
    assert b.deflection() == -SingularityFunction(x, 0, 2)/5625 + SingularityFunction(x, 0, 3)/5625\
                    - 133*SingularityFunction(x, 1, 3)/405000 + SingularityFunction(x, 3, 3)/3000\
                    - 37*SingularityFunction(x, 4, 3)/202500


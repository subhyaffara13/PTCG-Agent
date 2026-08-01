
def test_apply_rotation_hinge():
    b = Beam(15, 20, 20)
    r0, m0 = b.apply_support(0, type='fixed')
    r10 = b.apply_support(10, type='pin')
    r15 = b.apply_support(15, type='pin')
    p7 = b.apply_rotation_hinge(7)
    p12 = b.apply_rotation_hinge(12)
    b.apply_load(-10, 7, -1)
    b.apply_load(-2, 10, 0, 15)
    b.solve_for_reaction_loads(r0, m0, r10, r15)
    R_0, M_0, R_10, R_15, P_7, P_12 = symbols('R_0, M_0, R_10, R_15, P_7, P_12')
    expected_reactions = {R_0: 20/3, M_0: -140/3, R_10: 31/3, R_15: 3}
    expected_rotations = {P_7: 2281/2160, P_12: -5137/5184}
    reaction_symbols = [r0, m0, r10, r15]
    rotation_symbols = [p7, p12]
    tolerance = 1e-6
    assert all(abs(b.reaction_loads[r] - expected_reactions[r]) < tolerance for r in reaction_symbols)
    assert all(abs(b.rotation_jumps[r] - expected_rotations[r]) < tolerance for r in rotation_symbols)
    expected_bending_moment = (140 * SingularityFunction(x, 0, 0) / 3 - 20 * SingularityFunction(x, 0, 1) / 3
        - 11405 * SingularityFunction(x, 7, -1) / 27 + 10 * SingularityFunction(x, 7, 1)
        - 31 * SingularityFunction(x, 10, 1) / 3 + SingularityFunction(x, 10, 2)
        + 128425 * SingularityFunction(x, 12, -1) / 324 - 3 * SingularityFunction(x, 15, 1)
        - SingularityFunction(x, 15, 2))
    assert b.bending_moment().expand() == expected_bending_moment.expand()
    expected_slope = (-7*SingularityFunction(x, 0, 1)/60 + SingularityFunction(x, 0, 2)/120
        + 2281*SingularityFunction(x, 7, 0)/2160 - SingularityFunction(x, 7, 2)/80
        + 31*SingularityFunction(x, 10, 2)/2400 - SingularityFunction(x, 10, 3)/1200
        - 5137*SingularityFunction(x, 12, 0)/5184 + 3*SingularityFunction(x, 15, 2)/800
        + SingularityFunction(x, 15, 3)/1200)
    assert b.slope().expand() == expected_slope.expand()
    expected_deflection = (-7 * SingularityFunction(x, 0, 2) / 120 + SingularityFunction(x, 0, 3) / 360
        + 2281 * SingularityFunction(x, 7, 1) / 2160 - SingularityFunction(x, 7, 3) / 240
        + 31 * SingularityFunction(x, 10, 3) / 7200 - SingularityFunction(x, 10, 4) / 4800
        - 5137 * SingularityFunction(x, 12, 1) / 5184 + SingularityFunction(x, 15, 3) / 800
        + SingularityFunction(x, 15, 4) / 4800)
    assert b.deflection().expand() == expected_deflection.expand()

    E = Symbol('E')
    I = Symbol('I')
    F = Symbol('F')
    b = Beam(10, E, I)
    r0, m0 = b.apply_support(0, type="fixed")
    r10 = b.apply_support(10, type="pin")
    b.apply_rotation_hinge(6)
    b.apply_load(F, 8, -1)
    b.solve_for_reaction_loads(r0, m0, r10)
    assert b.reaction_loads == {R_0: -F/2, M_0: 3*F, R_10: -F/2}
    assert (b.bending_moment() == -3*F*SingularityFunction(x, 0, 0) + F*SingularityFunction(x, 0, 1)/2
            + 17*F*SingularityFunction(x, 6, -1) - F*SingularityFunction(x, 8, 1)
            + F*SingularityFunction(x, 10, 1)/2)
    expected_deflection = -(-3*F*SingularityFunction(x, 0, 2)/2 + F*SingularityFunction(x, 0, 3)/12
            + 17*F*SingularityFunction(x, 6, 1) - F*SingularityFunction(x, 8, 3)/6
            + F*SingularityFunction(x, 10, 3)/12)/(E*I)
    assert b.deflection().expand() == expected_deflection.expand()

    E = Symbol('E')
    I = Symbol('I')
    F = Symbol('F')
    l1 = Symbol('l1', positive=True)
    l2 = Symbol('l2', positive=True)
    l3 = Symbol('l3', positive=True)
    L = l1 + l2 + l3
    b = Beam(L, E, I)
    r0, m0 = b.apply_support(0, type="fixed")
    r1 = b.apply_support(L, type="pin")
    b.apply_rotation_hinge(l1)
    b.apply_load(F, l1+l2, -1)
    b.solve_for_reaction_loads(r0, m0, r1)
    assert b.reaction_loads[r0] == -F*l3/(l2 + l3)
    assert b.reaction_loads[m0] == F*l1*l3/(l2 + l3)
    assert b.reaction_loads[r1] == -F*l2/(l2 + l3)
    expected_bending_moment = (-F*l1*l3*SingularityFunction(x, 0, 0)/(l2 + l3)
            + F*l2*SingularityFunction(x, l1 + l2 + l3, 1)/(l2 + l3)
            + F*l3*SingularityFunction(x, 0, 1)/(l2 + l3) - F*SingularityFunction(x, l1 + l2, 1)
            - (-2*F*l1**3*l3 - 3*F*l1**2*l2*l3 - 3*F*l1**2*l3**2 + F*l2**3*l3 + 3*F*l2**2*l3**2 + 2*F*l2*l3**3)
            *SingularityFunction(x, l1, -1)/(6*l2**2 + 12*l2*l3 + 6*l3**2))
    assert simplify(b.bending_moment().expand()) == simplify(expected_bending_moment.expand())


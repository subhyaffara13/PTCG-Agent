
def test_apply_sliding_hinge():
    b = Beam(13, 20, 20)
    r0, m0 = b.apply_support(0, type="fixed")
    w8 = b.apply_sliding_hinge(8)
    r13 = b.apply_support(13, type="pin")
    b.apply_load(-10, 5, -1)
    b.solve_for_reaction_loads(r0, m0, r13)
    R_0, M_0, R_13, W_8 = symbols('R_0, M_0, R_13 W_8')
    assert b.reaction_loads == {R_0: 10, M_0: -50, R_13: 0}
    tolerance = 1e-6
    assert abs(b.deflection_jumps[w8] - 85/24) < tolerance
    assert (b.bending_moment() == 50*SingularityFunction(x, 0, 0) - 10*SingularityFunction(x, 0, 1)
            + 10*SingularityFunction(x, 5, 1) - 4250*SingularityFunction(x, 8, -2)/3)
    assert (b.deflection() == -SingularityFunction(x, 0, 2)/16 + SingularityFunction(x, 0, 3)/240
            - SingularityFunction(x, 5, 3)/240 + 85*SingularityFunction(x, 8, 0)/24)

    E = Symbol('E')
    I = Symbol('I')
    I2 = Symbol('I2')
    b1 = Beam(5, E, I)
    b2 = Beam(8, E, I2)
    b = b1.join(b2)
    r0, m0 = b.apply_support(0, type="fixed")
    b.apply_sliding_hinge(8)
    r13 = b.apply_support(13, type="pin")
    b.apply_load(-10, 5, -1)
    b.solve_for_reaction_loads(r0, m0, r13)
    W_8 = Symbol('W_8')
    assert b.deflection_jumps == {W_8: 4250/(3*E*I2)}

    E = Symbol('E')
    I = Symbol('I')
    q = Symbol('q')
    l1 = Symbol('l1', positive=True)
    l2 = Symbol('l2', positive=True)
    l3 = Symbol('l3', positive=True)
    L = l1 + l2 + l3
    b = Beam(L, E, I)
    r0 = b.apply_support(0, type="pin")
    r3 = b.apply_support(l1, type="pin")
    b.apply_sliding_hinge(l1 + l2)
    r10 = b.apply_support(L, type="pin")
    b.apply_load(q, 0, 0, l1)
    b.solve_for_reaction_loads(r0, r3, r10)
    assert (b.bending_moment() == l1*q*SingularityFunction(x, 0, 1)/2 + l1*q*SingularityFunction(x, l1, 1)/2
            - q*SingularityFunction(x, 0, 2)/2 + q*SingularityFunction(x, l1, 2)/2
            + (-l1**3*l2*q/24 - l1**3*l3*q/24)*SingularityFunction(x, l1 + l2, -2))
    assert b.deflection() ==(l1**3*q*x/24 - l1*q*SingularityFunction(x, 0, 3)/12
                             - l1*q*SingularityFunction(x, l1, 3)/12 + q*SingularityFunction(x, 0, 4)/24
                             - q*SingularityFunction(x, l1, 4)/24
                             + (l1**3*l2*q/24 + l1**3*l3*q/24)*SingularityFunction(x, l1 + l2, 0))/(E*I)


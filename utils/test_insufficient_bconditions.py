
def test_insufficient_bconditions():
    # Test cases when required number of boundary conditions
    # are not provided to solve the integration constants.
    L = symbols('L', positive=True)
    E, I, P, a3, a4 = symbols('E I P a3 a4')

    b = Beam(L, E, I, base_char='a')
    b.apply_load(R2, L, -1)
    b.apply_load(R1, 0, -1)
    b.apply_load(-P, L/2, -1)
    b.solve_for_reaction_loads(R1, R2)

    p = b.slope()
    q = P*SingularityFunction(x, 0, 2)/4 - P*SingularityFunction(x, L/2, 2)/2 + P*SingularityFunction(x, L, 2)/4
    assert p == q/(E*I) + a3

    p = b.deflection()
    q = P*SingularityFunction(x, 0, 3)/12 - P*SingularityFunction(x, L/2, 3)/6 + P*SingularityFunction(x, L, 3)/12
    assert p == q/(E*I) + a3*x + a4

    b.bc_deflection = [(0, 0)]
    p = b.deflection()
    q = a3*x + P*SingularityFunction(x, 0, 3)/12 - P*SingularityFunction(x, L/2, 3)/6 + P*SingularityFunction(x, L, 3)/12
    assert p == q/(E*I)

    b.bc_deflection = [(0, 0), (L, 0)]
    p = b.deflection()
    q = -L**2*P*x/16 + P*SingularityFunction(x, 0, 3)/12 - P*SingularityFunction(x, L/2, 3)/6 + P*SingularityFunction(x, L, 3)/12
    assert p == q/(E*I)


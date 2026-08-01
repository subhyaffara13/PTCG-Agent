
def test_statically_indeterminate():
    E = Symbol('E')
    I = Symbol('I')
    M1, M2 = symbols('M1, M2')
    F = Symbol('F')
    l = Symbol('l', positive=True)

    b5 = Beam(l, E, I)
    b5.bc_deflection = [(0, 0),(l, 0)]
    b5.bc_slope = [(0, 0),(l, 0)]

    b5.apply_load(R1, 0, -1)
    b5.apply_load(M1, 0, -2)
    b5.apply_load(R2, l, -1)
    b5.apply_load(M2, l, -2)
    b5.apply_load(-F, l/2, -1)

    b5.solve_for_reaction_loads(R1, R2, M1, M2)
    p = b5.reaction_loads
    q = {R1: F/2, R2: F/2, M1: -F*l/8, M2: F*l/8}
    assert p == q


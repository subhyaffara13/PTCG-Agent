
def test_max_shear_force():
    E = Symbol('E')
    I = Symbol('I')

    b = Beam(3, E, I)
    R, M = symbols('R, M')
    b.apply_load(R, 0, -1)
    b.apply_load(M, 0, -2)
    b.apply_load(2, 3, -1)
    b.apply_load(4, 2, -1)
    b.apply_load(2, 2, 0, end=3)
    b.solve_for_reaction_loads(R, M)
    assert b.max_shear_force() == (Interval(0, 2), 8)

    l = symbols('l', positive=True)
    P = Symbol('P')
    b = Beam(l, E, I)
    R1, R2 = symbols('R1, R2')
    b.apply_load(R1, 0, -1)
    b.apply_load(R2, l, -1)
    b.apply_load(P, 0, 0, end=l)
    b.solve_for_reaction_loads(R1, R2)
    max_shear = b.max_shear_force()
    assert max_shear[0] == 0
    assert simplify(max_shear[1] - (l*Abs(P)/2)) == 0



def test_max_deflection():
    E, I, l, F = symbols('E, I, l, F', positive=True)
    b = Beam(l, E, I)
    b.bc_deflection = [(0, 0),(l, 0)]
    b.bc_slope = [(0, 0),(l, 0)]
    b.apply_load(F/2, 0, -1)
    b.apply_load(-F*l/8, 0, -2)
    b.apply_load(F/2, l, -1)
    b.apply_load(F*l/8, l, -2)
    b.apply_load(-F, l/2, -1)
    assert b.max_deflection() == (l/2, F*l**3/(192*E*I))


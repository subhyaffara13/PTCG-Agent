
def test_max_bending_moment_Beam3D():
    x = symbols('x')
    b = Beam3D(20, 40, 21, 100, 25)
    b.apply_load(15, start=0, order=0, dir="z")
    b.apply_load(12*x, start=0, order=0, dir="y")
    b.bc_deflection = [(0, [0, 0, 0]), (20, [0, 0, 0])]
    assert b.max_bmoment() == [(0, 0), (20, 3000), (20, 16000)]


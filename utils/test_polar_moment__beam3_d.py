
def test_polar_moment_Beam3D():
    l, E, G, A, I1, I2 = symbols('l, E, G, A, I1, I2')
    I = [I1, I2]

    b = Beam3D(l, E, G, I, A)
    assert b.polar_moment() == I1 + I2



def test_symmetrize():
    assert symmetrize(0, x, y, z) == (0, 0)
    assert symmetrize(1, x, y, z) == (1, 0)

    s1 = x + y + z
    s2 = x*y + x*z + y*z

    assert symmetrize(1) == (1, 0)
    assert symmetrize(1, formal=True) == (1, 0, [])

    assert symmetrize(x) == (x, 0)
    assert symmetrize(x + 1) == (x + 1, 0)

    assert symmetrize(x, x, y) == (x + y, -y)
    assert symmetrize(x + 1, x, y) == (x + y + 1, -y)

    assert symmetrize(x, x, y, z) == (s1, -y - z)
    assert symmetrize(x + 1, x, y, z) == (s1 + 1, -y - z)

    assert symmetrize(x**2, x, y, z) == (s1**2 - 2*s2, -y**2 - z**2)

    assert symmetrize(x**2 + y**2) == (-2*x*y + (x + y)**2, 0)
    assert symmetrize(x**2 - y**2) == (-2*x*y + (x + y)**2, -2*y**2)

    assert symmetrize(x**3 + y**2 + a*x**2 + b*y**3, x, y) == \
        (-3*x*y*(x + y) - 2*a*x*y + a*(x + y)**2 + (x + y)**3,
         y**2*(1 - a) + y**3*(b - 1))

    U = [u0, u1, u2] = symbols('u:3')

    assert symmetrize(x + 1, x, y, z, formal=True, symbols=U) == \
        (u0 + 1, -y - z, [(u0, x + y + z), (u1, x*y + x*z + y*z), (u2, x*y*z)])

    assert symmetrize([1, 2, 3]) == [(1, 0), (2, 0), (3, 0)]
    assert symmetrize([1, 2, 3], formal=True) == ([(1, 0), (2, 0), (3, 0)], [])

    assert symmetrize([x + y, x - y]) == [(x + y, 0), (x + y, -2*y)]


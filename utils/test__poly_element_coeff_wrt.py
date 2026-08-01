
def test_PolyElement_coeff_wrt():
    R, x, y, z = ring("x, y, z", ZZ)

    p = 4*x**3 + 5*y**2 + 6*y**2*z + 7
    assert p.coeff_wrt(1, 2) == 6*z + 5 # using generator index
    assert p.coeff_wrt(x, 3) == 4 # using generator

    p = 2*x**4 + 3*x*y**2*z + 10*y**2 + 10*x*z**2
    assert p.coeff_wrt(x, 1) == 3*y**2*z + 10*z**2
    assert p.coeff_wrt(y, 2) == 3*x*z + 10

    p = 4*x**2 + 2*x*y + 5
    assert p.coeff_wrt(z, 1) == R(0)
    assert p.coeff_wrt(y, 2) == R(0)


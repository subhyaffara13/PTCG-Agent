
def test_Poly_homogenize():
    assert Poly(x**2+y).homogenize(z) == Poly(x**2+y*z)
    assert Poly(x+y).homogenize(z) == Poly(x+y, x, y, z)
    assert Poly(x+y**2).homogenize(y) == Poly(x*y+y**2)


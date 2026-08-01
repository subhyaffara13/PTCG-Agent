
def test_Poly_lift():
    p = Poly(x**4 - I*x + 17*I, x, gaussian=True)
    assert p.lift() == Poly(x**8 + x**2 - 34*x + 289, x, domain='QQ')


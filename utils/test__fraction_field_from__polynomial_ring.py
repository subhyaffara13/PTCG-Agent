
def test_FractionField_from_PolynomialRing():
    R, x,y = ring("x,y", QQ)
    F, X,Y = field("x,y", ZZ)

    f = 3*x**2 + 5*y**2
    g = x**2/3 + y**2/5

    assert F.to_domain().from_PolynomialRing(f, R.to_domain()) == 3*X**2 + 5*Y**2
    assert F.to_domain().from_PolynomialRing(g, R.to_domain()) == (5*X**2 + 3*Y**2)/15


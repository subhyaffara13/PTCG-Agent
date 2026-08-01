
def test_PolynomialRing_from_FractionField():
    F, x,y = field("x,y", ZZ)
    R, X,Y = ring("x,y", ZZ)

    f = (x**2 + y**2)/(x + 1)
    g = (x**2 + y**2)/4
    h =  x**2 + y**2

    assert R.to_domain().from_FractionField(f, F.to_domain()) is None
    assert R.to_domain().from_FractionField(g, F.to_domain()) == X**2/4 + Y**2/4
    assert R.to_domain().from_FractionField(h, F.to_domain()) == X**2 + Y**2

    F, x,y = field("x,y", QQ)
    R, X,Y = ring("x,y", QQ)

    f = (x**2 + y**2)/(x + 1)
    g = (x**2 + y**2)/4
    h =  x**2 + y**2

    assert R.to_domain().from_FractionField(f, F.to_domain()) is None
    assert R.to_domain().from_FractionField(g, F.to_domain()) == X**2/4 + Y**2/4
    assert R.to_domain().from_FractionField(h, F.to_domain()) == X**2 + Y**2


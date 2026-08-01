
def test_primitive():
    f, g = 4*x + 2, 2*x + 1
    F, G = Poly(f), Poly(g)

    assert F.primitive() == (2, G)
    assert primitive(f) == (2, g)
    assert primitive(f, x) == (2, g)
    assert primitive(f, (x,)) == (2, g)
    assert primitive(F) == (2, G)
    assert primitive(f, polys=True) == (2, G)
    assert primitive(F, polys=False) == (2, g)

    raises(ComputationFailed, lambda: primitive(4))

    f = Poly(2*x, modulus=3)
    g = Poly(2.0*x, domain=RR)

    assert f.primitive() == (1, f)
    assert g.primitive() == (1.0, g)

    assert primitive(S('-3*x/4 + y + 11/8')) == \
        S('(1/8, -6*x + 8*y + 11)')


def test_primitive():
    assert (3*(x + 1)**2).primitive() == (3, (x + 1)**2)
    assert (6*x + 2).primitive() == (2, 3*x + 1)
    assert (x/2 + 3).primitive() == (S.Half, x + 6)
    eq = (6*x + 2)*(x/2 + 3)
    assert eq.primitive()[0] == 1
    eq = (2 + 2*x)**2
    assert eq.primitive()[0] == 1
    assert (4.0*x).primitive() == (1, 4.0*x)
    assert (4.0*x + y/2).primitive() == (S.Half, 8.0*x + y)
    assert (-2*x).primitive() == (2, -x)
    assert Add(5*z/7, 0.5*x, 3*y/2, evaluate=False).primitive() == \
        (S.One/14, 7.0*x + 21*y + 10*z)
    for i in [S.Infinity, S.NegativeInfinity, S.ComplexInfinity]:
        assert (i + x/3).primitive() == \
            (S.One/3, i + x)
    assert (S.Infinity + 2*x/3 + 4*y/7).primitive() == \
        (S.One/21, 14*x + 12*y + oo)
    assert S.Zero.primitive() == (S.One, S.Zero)


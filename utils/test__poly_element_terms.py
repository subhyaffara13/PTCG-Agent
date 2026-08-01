
def test_PolyElement_terms():
    R, x,y,z = ring("x,y,z", QQ)
    terms = (x**2/3 + y**3/4 + z**4/5).terms()
    assert terms == [((2,0,0), QQ(1,3)), ((0,3,0), QQ(1,4)), ((0,0,4), QQ(1,5))]

    R, x,y = ring("x,y", ZZ, lex)
    f = x*y**7 + 2*x**2*y**3

    assert f.terms() == f.terms(lex) == f.terms('lex') == [((2, 3), 2), ((1, 7), 1)]
    assert f.terms(grlex) == f.terms('grlex') == [((1, 7), 1), ((2, 3), 2)]

    R, x,y = ring("x,y", ZZ, grlex)
    f = x*y**7 + 2*x**2*y**3

    assert f.terms() == f.terms(grlex) == f.terms('grlex') == [((1, 7), 1), ((2, 3), 2)]
    assert f.terms(lex) == f.terms('lex') == [((2, 3), 2), ((1, 7), 1)]

    R, = ring("", ZZ)
    assert R(3).terms() == [((), 3)]


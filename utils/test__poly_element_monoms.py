
def test_PolyElement_monoms():
    R, x,y,z = ring("x,y,z", QQ)
    monoms = (x**2/3 + y**3/4 + z**4/5).monoms()
    assert monoms == [(2,0,0), (0,3,0), (0,0,4)]

    R, x,y = ring("x,y", ZZ, lex)
    f = x*y**7 + 2*x**2*y**3

    assert f.monoms() == f.monoms(lex) == f.monoms('lex') == [(2, 3), (1, 7)]
    assert f.monoms(grlex) == f.monoms('grlex') == [(1, 7), (2, 3)]

    R, x,y = ring("x,y", ZZ, grlex)
    f = x*y**7 + 2*x**2*y**3

    assert f.monoms() == f.monoms(grlex) == f.monoms('grlex') == [(1, 7), (2, 3)]
    assert f.monoms(lex) == f.monoms('lex') == [(2, 3), (1, 7)]


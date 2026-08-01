
def test_Infinity_2():
    x = Symbol('x')
    assert oo*x != oo
    assert oo*(pi - 1) is oo
    assert oo*(1 - pi) is -oo

    assert (-oo)*x != -oo
    assert (-oo)*(pi - 1) is -oo
    assert (-oo)*(1 - pi) is oo

    assert (-1)**S.NaN is S.NaN
    assert oo - _inf is S.NaN
    assert oo + _ninf is S.NaN
    assert oo*0 is S.NaN
    assert oo/_inf is S.NaN
    assert oo/_ninf is S.NaN
    assert oo**S.NaN is S.NaN
    assert -oo + _inf is S.NaN
    assert -oo - _ninf is S.NaN
    assert -oo*S.NaN is S.NaN
    assert -oo*0 is S.NaN
    assert -oo/_inf is S.NaN
    assert -oo/_ninf is S.NaN
    assert -oo/S.NaN is S.NaN
    assert abs(-oo) is oo
    assert all((-oo)**i is S.NaN for i in (oo, -oo, S.NaN))
    assert (-oo)**3 is -oo
    assert (-oo)**2 is oo
    assert abs(S.ComplexInfinity) is oo


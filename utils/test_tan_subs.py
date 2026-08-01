
def test_tan_subs():
    assert tan(x).subs(tan(x), y) == y
    assert tan(x).subs(x, y) == tan(y)
    assert tan(x).subs(x, S.Pi/2) is zoo
    assert tan(x).subs(x, S.Pi*Rational(3, 2)) is zoo


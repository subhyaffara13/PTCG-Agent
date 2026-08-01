
def test_issue_10102():
    assert limit(fresnels(x), x, oo) == S.Half
    assert limit(3 + fresnels(x), x, oo) == 3 + S.Half
    assert limit(5*fresnels(x), x, oo) == Rational(5, 2)
    assert limit(fresnelc(x), x, oo) == S.Half
    assert limit(fresnels(x), x, -oo) == Rational(-1, 2)
    assert limit(4*fresnelc(x), x, -oo) == -2


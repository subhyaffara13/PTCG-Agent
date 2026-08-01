
def test_Integers_eval_imageset():
    ans = ImageSet(Lambda(x, 2*x + Rational(3, 7)), S.Integers)
    im = imageset(Lambda(x, -2*x + Rational(3, 7)), S.Integers)
    assert im == ans
    im = imageset(Lambda(x, -2*x - Rational(11, 7)), S.Integers)
    assert im == ans
    y = Symbol('y')
    L = imageset(x, 2*x + y, S.Integers)
    assert y + 4 in L
    a, b, c = 0.092, 0.433, 0.341
    assert a in imageset(x, a + c*x, S.Integers)
    assert b in imageset(x, b + c*x, S.Integers)

    _x = symbols('x', negative=True)
    eq = _x**2 - _x + 1
    assert imageset(_x, eq, S.Integers).lamda.expr == _x**2 + _x + 1
    eq = 3*_x - 1
    assert imageset(_x, eq, S.Integers).lamda.expr == 3*_x + 2

    assert imageset(x, (x, 1/x), S.Integers) == \
        ImageSet(Lambda(x, (x, 1/x)), S.Integers)


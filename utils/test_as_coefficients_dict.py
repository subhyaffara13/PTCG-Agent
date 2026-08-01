
def test_as_coefficients_dict():
    check = [S.One, x, y, x*y, 1]
    assert [Add(3*x, 2*x, y, 3).as_coefficients_dict()[i] for i in check] == \
        [3, 5, 1, 0, 3]
    assert [Add(3*x, 2*x, y, 3, evaluate=False).as_coefficients_dict()[i]
            for i in check] == [3, 5, 1, 0, 3]
    assert [(3*x*y).as_coefficients_dict()[i] for i in check] == \
        [0, 0, 0, 3, 0]
    assert [(3.0*x*y).as_coefficients_dict()[i] for i in check] == \
        [0, 0, 0, 3.0, 0]
    assert (3.0*x*y).as_coefficients_dict()[3.0*x*y] == 0
    eq = x*(x + 1)*a + x*b + c/x
    assert eq.as_coefficients_dict(x) == {x: b, 1/x: c,
        x*(x + 1): a}
    assert eq.expand().as_coefficients_dict(x) == {x**2: a, x: a + b, 1/x: c}
    assert x.as_coefficients_dict() == {x: S.One}


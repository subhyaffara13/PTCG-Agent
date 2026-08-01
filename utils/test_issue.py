
def test_issue():
    # https://github.com/sympy/sympy/issues/10191
    # https://github.com/sympy/sympy/issues/19543

    a, b = symbols('a b')
    assert rs_series(sin(a**QQ(3,7))*exp(a + b**QQ(6,7)), a,2).as_expr() == \
        a**QQ(10,7)*exp(b**QQ(6,7)) - a**QQ(9,7)*exp(b**QQ(6,7))/6 + a**QQ(3,7)*exp(b**QQ(6,7))



def test_issue_11313():
    assert Integral(cos(x), x).series(x) == sin(x).series(x)
    assert Derivative(sin(x), x).series(x, n=3).doit() == cos(x).series(x, n=3)

    assert Derivative(x**3, x).as_leading_term(x) == 3*x**2
    assert Derivative(x**3, y).as_leading_term(x) == 0
    assert Derivative(sin(x), x).as_leading_term(x) == 1
    assert Derivative(cos(x), x).as_leading_term(x) == -x

    # This result is equivalent to zero, zero is not return because
    # `Expr.series` doesn't currently detect an `x` in its `free_symbol`s.
    assert Derivative(1, x).as_leading_term(x) == Derivative(1, x)

    assert Derivative(exp(x), x).series(x).doit() == exp(x).series(x)
    assert 1 + Integral(exp(x), x).series(x) == exp(x).series(x)

    assert Derivative(log(x), x).series(x).doit() == (1/x).series(x)
    assert Integral(log(x), x).series(x) == Integral(log(x), x).doit().series(x).removeO()


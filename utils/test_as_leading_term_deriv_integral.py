
def test_as_leading_term_deriv_integral():
    # related to issue 11313
    assert Derivative(x ** 3, x).as_leading_term(x) == 3*x**2
    assert Derivative(x ** 3, y).as_leading_term(x) == 0

    assert Integral(x ** 3, x).as_leading_term(x) == x**4/4
    assert Integral(x ** 3, y).as_leading_term(x) == y*x**3

    assert Derivative(exp(x), x).as_leading_term(x) == 1
    assert Derivative(log(x), x).as_leading_term(x) == (1/x).as_leading_term(x)


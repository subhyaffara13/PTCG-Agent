
def test_derivatives_matrix_norms():

    expr = x.T*y
    assert expr.diff(x) == y
    assert expr[0, 0].diff(x[m, 0]).doit() == y[m, 0]

    expr = (x.T*y)**S.Half
    assert expr.diff(x) == y/(2*sqrt(x.T*y))

    expr = (x.T*x)**S.Half
    assert expr.diff(x) == x*(x.T*x)**Rational(-1, 2)

    expr = (c.T*a*x.T*b)**S.Half
    assert expr.diff(x) == b*a.T*c/sqrt(c.T*a*x.T*b)/2

    expr = (c.T*a*x.T*b)**Rational(1, 3)
    assert expr.diff(x) == b*a.T*c*(c.T*a*x.T*b)**Rational(-2, 3)/3

    expr = (a.T*X*b)**S.Half
    assert expr.diff(X) == a/(2*sqrt(a.T*X*b))*b.T

    expr = d.T*x*(a.T*X*b)**S.Half*y.T*c
    assert expr.diff(X) == a/(2*sqrt(a.T*X*b))*x.T*d*y.T*c*b.T


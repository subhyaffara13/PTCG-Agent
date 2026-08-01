
def test_log_product():
    from sympy.abc import n, m

    i, j = symbols('i,j', positive=True, integer=True)
    x, y = symbols('x,y', positive=True)
    z = symbols('z', real=True)
    w = symbols('w')

    expr = log(Product(x**i, (i, 1, n)))
    assert simplify(expr) == expr
    assert expr.expand() == Sum(i*log(x), (i, 1, n))
    expr = log(Product(x**i*y**j, (i, 1, n), (j, 1, m)))
    assert simplify(expr) == expr
    assert expr.expand() == Sum(i*log(x) + j*log(y), (i, 1, n), (j, 1, m))

    expr = log(Product(-2, (n, 0, 4)))
    assert simplify(expr) == expr
    assert expr.expand() == expr
    assert expr.expand(force=True) == Sum(log(-2), (n, 0, 4))

    expr = log(Product(exp(z*i), (i, 0, n)))
    assert expr.expand() == Sum(z*i, (i, 0, n))

    expr = log(Product(exp(w*i), (i, 0, n)))
    assert expr.expand() == expr
    assert expr.expand(force=True) == Sum(w*i, (i, 0, n))

    expr = log(Product(i**2*abs(j), (i, 1, n), (j, 1, m)))
    assert expr.expand() == Sum(2*log(i) + log(j), (i, 1, n), (j, 1, m))


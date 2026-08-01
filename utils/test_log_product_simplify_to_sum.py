
def test_log_product_simplify_to_sum():
    from sympy.abc import n, m
    i, j = symbols('i,j', positive=True, integer=True)
    x, y = symbols('x,y', positive=True)
    assert simplify(log(Product(x**i, (i, 1, n)))) == Sum(i*log(x), (i, 1, n))
    assert simplify(log(Product(x**i*y**j, (i, 1, n), (j, 1, m)))) == \
            Sum(i*log(x) + j*log(y), (i, 1, n), (j, 1, m))



def test_expand_with_assumptions():
    M = Symbol('M', integer=True, positive=True)
    x = Symbol('x', positive=True)
    m = Symbol('m', nonnegative=True)
    assert log(Product(x**m, (m, 0, M))).expand() == Sum(m*log(x), (m, 0, M))
    assert log(Product(exp(x**m), (m, 0, M))).expand() == Sum(x**m, (m, 0, M))
    assert log(Product(x**m, (m, 0, M))).rewrite(Sum).expand() == Sum(m*log(x), (m, 0, M))
    assert log(Product(exp(x**m), (m, 0, M))).rewrite(Sum).expand() == Sum(x**m, (m, 0, M))

    n = Symbol('n', nonnegative=True)
    i, j = symbols('i,j', positive=True, integer=True)
    x, y = symbols('x,y', positive=True)
    assert log(Product(x**i*y**j, (i, 1, n), (j, 1, m))).expand() \
        == Sum(i*log(x) + j*log(y), (i, 1, n), (j, 1, m))

    m = Symbol('m', nonnegative=True, integer=True)
    s = Sum(x**m, (m, 0, M))
    s_as_product = s.rewrite(Product)
    assert s_as_product.has(Product)
    assert s_as_product == log(Product(exp(x**m), (m, 0, M)))
    assert s_as_product.expand() == s
    s5 = s.subs(M, 5)
    s5_as_product = s5.rewrite(Product)
    assert s5_as_product.has(Product)
    assert s5_as_product.doit().expand() == s5.doit()


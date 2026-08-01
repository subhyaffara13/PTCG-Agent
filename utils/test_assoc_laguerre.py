
def test_assoc_laguerre():
    n = Symbol("n")
    m = Symbol("m")
    alpha = Symbol("alpha")

    # generalized Laguerre polynomials:
    assert assoc_laguerre(0, alpha, x) == 1
    assert assoc_laguerre(1, alpha, x) == -x + alpha + 1
    assert assoc_laguerre(2, alpha, x).expand() == \
        (x**2/2 - (alpha + 2)*x + (alpha + 2)*(alpha + 1)/2).expand()
    assert assoc_laguerre(3, alpha, x).expand() == \
        (-x**3/6 + (alpha + 3)*x**2/2 - (alpha + 2)*(alpha + 3)*x/2 +
        (alpha + 1)*(alpha + 2)*(alpha + 3)/6).expand()

    # Test the lowest 10 polynomials with laguerre_poly, to make sure it works:
    for i in range(10):
        assert assoc_laguerre(i, 0, x).expand() == laguerre_poly(i, x)

    X = assoc_laguerre(n, m, x)
    assert isinstance(X, assoc_laguerre)

    assert assoc_laguerre(n, 0, x) == laguerre(n, x)
    assert assoc_laguerre(n, alpha, 0) == binomial(alpha + n, alpha)
    p = Symbol("p", positive=True)
    assert assoc_laguerre(p, alpha, oo) == (-1)**p*oo
    assert assoc_laguerre(p, alpha, -oo) is oo

    assert diff(assoc_laguerre(n, alpha, x), x) == \
        -assoc_laguerre(n - 1, alpha + 1, x)
    _k = Dummy('k')
    assert diff(assoc_laguerre(n, alpha, x), alpha).dummy_eq(
        Sum(assoc_laguerre(_k, alpha, x)/(-alpha + n), (_k, 0, n - 1)))

    assert conjugate(assoc_laguerre(n, alpha, x)) == \
        assoc_laguerre(n, conjugate(alpha), conjugate(x))

    assert assoc_laguerre(n, alpha, x).rewrite(Sum).dummy_eq(
            gamma(alpha + n + 1)*Sum(x**_k*RisingFactorial(-n, _k)/
            (factorial(_k)*gamma(_k + alpha + 1)), (_k, 0, n))/factorial(n))
    assert assoc_laguerre(n, alpha, x).rewrite("polynomial").dummy_eq(
            gamma(alpha + n + 1)*Sum(x**_k*RisingFactorial(-n, _k)/
            (factorial(_k)*gamma(_k + alpha + 1)), (_k, 0, n))/factorial(n))
    raises(ValueError, lambda: assoc_laguerre(-2.1, alpha, x))
    raises(ArgumentIndexError, lambda: assoc_laguerre(n, alpha, x).fdiff(1))
    raises(ArgumentIndexError, lambda: assoc_laguerre(n, alpha, x).fdiff(4))


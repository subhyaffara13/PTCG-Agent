
def test__eval_product():
    from sympy.abc import i, n
    # issue 4809
    a = Function('a')
    assert product(2*a(i), (i, 1, n)) == 2**n * Product(a(i), (i, 1, n))
    # issue 4810
    assert product(2**i, (i, 1, n)) == 2**(n*(n + 1)/2)
    k, m = symbols('k m', integer=True)
    assert product(2**i, (i, k, m)) == 2**(-k**2/2 + k/2 + m**2/2 + m/2)
    n = Symbol('n', negative=True, integer=True)
    p = Symbol('p', positive=True, integer=True)
    assert product(2**i, (i, n, p)) == 2**(-n**2/2 + n/2 + p**2/2 + p/2)
    assert product(2**i, (i, p, n)) == 2**(n**2/2 + n/2 - p**2/2 + p/2)


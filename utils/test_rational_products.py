
def test_rational_products():
    assert product(1 + 1/k, (k, 1, n)) == rf(2, n)/factorial(n)


def test_rational_products():
    assert combsimp(product(1 + 1/n, (n, a, b))) == (1 + b)/a
    assert combsimp(product(n + 1, (n, a, b))) == gamma(2 + b)/gamma(1 + a)
    assert combsimp(product((n + 1)/(n - 1), (n, a, b))) == b*(1 + b)/(a*(a - 1))
    assert combsimp(product(n/(n + 1)/(n + 2), (n, a, b))) == \
        a*gamma(a + 2)/(b + 1)/gamma(b + 3)
    assert combsimp(product(n*(n + 1)/(n - 1)/(n - 2), (n, a, b))) == \
        b**2*(b - 1)*(1 + b)/(a - 1)**2/(a*(a - 2))


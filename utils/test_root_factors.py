
def test_root_factors():
    assert root_factors(Poly(1, x)) == [Poly(1, x)]
    assert root_factors(Poly(x, x)) == [Poly(x, x)]

    assert root_factors(x**2 - 1, x) == [x + 1, x - 1]
    assert root_factors(x**2 - y, x) == [x - sqrt(y), x + sqrt(y)]

    assert root_factors((x**4 - 1)**2) == \
        [x + 1, x + 1, x - 1, x - 1, x - I, x - I, x + I, x + I]

    assert root_factors(Poly(x**4 - 1, x), filter='Z') == \
        [Poly(x + 1, x), Poly(x - 1, x), Poly(x**2 + 1, x)]
    assert root_factors(8*x**2 + 12*x**4 + 6*x**6 + x**8, x, filter='Q') == \
        [x, x, x**6 + 6*x**4 + 12*x**2 + 8]


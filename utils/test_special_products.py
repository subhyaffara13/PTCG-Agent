
def test_special_products():
    # Wallis product
    assert product((4*k)**2 / (4*k**2 - 1), (k, 1, n)) == \
        4**n*factorial(n)**2/rf(S.Half, n)/rf(Rational(3, 2), n)

    # Euler's product formula for sin
    assert product(1 + a/k**2, (k, 1, n)) == \
        rf(1 - sqrt(-a), n)*rf(1 + sqrt(-a), n)/factorial(n)**2


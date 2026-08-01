
def test_simple_products():
    assert product(2, (k, a, n)) == 2**(n - a + 1)
    assert product(k, (k, 1, n)) == factorial(n)
    assert product(k**3, (k, 1, n)) == factorial(n)**3

    assert product(k + 1, (k, 0, n - 1)) == factorial(n)
    assert product(k + 1, (k, a, n - 1)) == rf(1 + a, n - a)

    assert product(cos(k), (k, 0, 5)) == cos(1)*cos(2)*cos(3)*cos(4)*cos(5)
    assert product(cos(k), (k, 3, 5)) == cos(3)*cos(4)*cos(5)
    assert product(cos(k), (k, 1, Rational(5, 2))) != cos(1)*cos(2)

    assert isinstance(product(k**k, (k, 1, n)), Product)

    assert Product(x**k, (k, 1, n)).variables == [k]

    raises(ValueError, lambda: Product(n))
    raises(ValueError, lambda: Product(n, k))
    raises(ValueError, lambda: Product(n, k, 1))
    raises(ValueError, lambda: Product(n, k, 1, 10))
    raises(ValueError, lambda: Product(n, (k, 1)))

    assert product(1, (n, 1, oo)) == 1  # issue 8301
    assert product(2, (n, 1, oo)) is oo
    assert product(-1, (n, 1, oo)).func is Product


def test_simple_products():
    assert Product(S.NaN, (x, 1, 3)) is S.NaN
    assert product(S.NaN, (x, 1, 3)) is S.NaN
    assert Product(x, (n, a, a)).doit() == x
    assert Product(x, (x, a, a)).doit() == a
    assert Product(x, (y, 1, a)).doit() == x**a

    lo, hi = 1, 2
    s1 = Product(n, (n, lo, hi))
    s2 = Product(n, (n, hi, lo))
    assert s1 != s2
    # This IS correct according to Karr product convention
    assert s1.doit() == 2
    assert s2.doit() == 1

    lo, hi = x, x + 1
    s1 = Product(n, (n, lo, hi))
    s2 = Product(n, (n, hi, lo))
    s3 = 1 / Product(n, (n, hi + 1, lo - 1))
    assert s1 != s2
    # This IS correct according to Karr product convention
    assert s1.doit() == x*(x + 1)
    assert s2.doit() == 1
    assert s3.doit() == x*(x + 1)

    assert Product(Integral(2*x, (x, 1, y)) + 2*x, (x, 1, 2)).doit() == \
        (y**2 + 1)*(y**2 + 3)
    assert product(2, (n, a, b)) == 2**(b - a + 1)
    assert product(n, (n, 1, b)) == factorial(b)
    assert product(n**3, (n, 1, b)) == factorial(b)**3
    assert product(3**(2 + n), (n, a, b)) \
        == 3**(2*(1 - a + b) + b/2 + (b**2)/2 + a/2 - (a**2)/2)
    assert product(cos(n), (n, 3, 5)) == cos(3)*cos(4)*cos(5)
    assert product(cos(n), (n, x, x + 2)) == cos(x)*cos(x + 1)*cos(x + 2)
    assert isinstance(product(cos(n), (n, x, x + S.Half)), Product)
    # If Product managed to evaluate this one, it most likely got it wrong!
    assert isinstance(Product(n**n, (n, 1, b)), Product)



def test_multiple_products():
    assert product(x, (n, 1, k), (k, 1, m)) == x**(m**2/2 + m/2)
    assert product(f(n), (
        n, 1, m), (m, 1, k)) == Product(f(n), (n, 1, m), (m, 1, k)).doit()
    assert Product(f(n), (m, 1, k), (n, 1, k)).doit() == \
        Product(Product(f(n), (m, 1, k)), (n, 1, k)).doit() == \
        product(f(n), (m, 1, k), (n, 1, k)) == \
        product(product(f(n), (m, 1, k)), (n, 1, k)) == \
        Product(f(n)**k, (n, 1, k))
    assert Product(
        x, (x, 1, k), (k, 1, n)).doit() == Product(factorial(k), (k, 1, n))

    assert Product(x**k, (n, 1, k), (k, 1, m)).variables == [n, k]


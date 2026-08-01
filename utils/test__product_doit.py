
def test_Product_doit():
    assert Product(n*Integral(a**2), (n, 1, 3)).doit() == 2 * a**9 / 9
    assert Product(n*Integral(a**2), (n, 1, 3)).doit(deep=False) == \
        6*Integral(a**2)**3
    assert product(n*Integral(a**2), (n, 1, 3)) == 6*Integral(a**2)**3


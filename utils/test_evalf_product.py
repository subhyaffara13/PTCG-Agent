
def test_evalf_product():
    assert Product(n, (n, 1, 10)).evalf() == 3628800.
    assert comp(Product(1 - S.Half**2/n**2, (n, 1, oo)).n(5), 0.63662)
    assert Product(n, (n, -1, 3)).evalf() == 0


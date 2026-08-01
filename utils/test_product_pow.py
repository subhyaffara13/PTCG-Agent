
def test_product_pow():
    # issue 4817
    assert product(2**f(k), (k, 1, n)) == 2**Sum(f(k), (k, 1, n))
    assert product(2**(2*f(k)), (k, 1, n)) == 2**Sum(2*f(k), (k, 1, n))



def test_infinite_product():
    # issue 5737
    assert isinstance(Product(2**(1/factorial(n)), (n, 0, oo)), Product)


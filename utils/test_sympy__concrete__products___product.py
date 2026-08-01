
def test_sympy__concrete__products__Product():
    from sympy.concrete.products import Product
    assert _test_args(Product(x, (x, 0, 10)))
    assert _test_args(Product(x, (x, 0, y), (y, 0, 10)))


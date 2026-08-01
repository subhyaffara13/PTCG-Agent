
def test_Product():
    assert precedence(Product(x, (x, y, y + 1))) == PRECEDENCE["Atom"]


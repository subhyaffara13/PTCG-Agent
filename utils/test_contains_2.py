
def test_contains_2():
    assert Order(x).contains(Order(y)) is None
    assert Order(x).contains(Order(y*x))
    assert Order(y*x).contains(Order(x))
    assert Order(y).contains(Order(x*y))
    assert Order(x).contains(Order(y**2*x))


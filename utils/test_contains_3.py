
def test_contains_3():
    assert Order(x*y**2).contains(Order(x**2*y)) is None
    assert Order(x**2*y).contains(Order(x*y**2)) is None


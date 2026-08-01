
def test_contains_0():
    assert Order(1, x).contains(Order(1, x))
    assert Order(1, x).contains(Order(1))
    assert Order(1).contains(Order(1, x)) is False


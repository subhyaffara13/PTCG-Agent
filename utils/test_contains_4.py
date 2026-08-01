
def test_contains_4():
    assert Order(sin(1/x**2)).contains(Order(cos(1/x**2))) is True
    assert Order(cos(1/x**2)).contains(Order(sin(1/x**2))) is True


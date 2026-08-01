
def test_contains_1():
    assert Order(x).contains(Order(x))
    assert Order(x).contains(Order(x**2))
    assert not Order(x**2).contains(Order(x))
    assert not Order(x).contains(Order(1/x))
    assert not Order(1/x).contains(Order(exp(1/x)))
    assert not Order(x).contains(Order(exp(1/x)))
    assert Order(1/x).contains(Order(x))
    assert Order(exp(1/x)).contains(Order(x))
    assert Order(exp(1/x)).contains(Order(1/x))
    assert Order(exp(1/x)).contains(Order(exp(1/x)))
    assert Order(exp(2/x)).contains(Order(exp(1/x)))
    assert not Order(exp(1/x)).contains(Order(exp(2/x)))


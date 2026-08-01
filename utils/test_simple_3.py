
def test_simple_3():
    assert Order(x) + x == Order(x)
    assert Order(x) + 2 == 2 + Order(x)
    assert Order(x) + x**2 == Order(x)
    assert Order(x) + 1/x == 1/x + Order(x)
    assert Order(1/x) + 1/x**2 == 1/x**2 + Order(1/x)
    assert Order(x) + exp(1/x) == Order(x) + exp(1/x)


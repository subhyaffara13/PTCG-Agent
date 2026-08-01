
def test_simple_5():
    assert Order(x) + Order(x**2) == Order(x)
    assert Order(x) + Order(x**-2) == Order(x**-2)
    assert Order(x) + Order(1/x) == Order(1/x)


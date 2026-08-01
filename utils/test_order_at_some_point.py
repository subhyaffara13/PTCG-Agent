
def test_order_at_some_point():
    assert Order(x, (x, 1)) == Order(1, (x, 1))
    assert Order(2*x - 2, (x, 1)) == Order(x - 1, (x, 1))
    assert Order(-x + 1, (x, 1)) == Order(x - 1, (x, 1))
    assert Order(x - 1, (x, 1))**2 == Order((x - 1)**2, (x, 1))
    assert Order(x - 2, (x, 2)) - O(x - 2, (x, 2)) == Order(x - 2, (x, 2))


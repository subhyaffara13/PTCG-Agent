
def test_mixing_order_at_zero_and_infinity():
    assert (Order(x, (x, 0)) + Order(x, (x, oo))).is_Add
    assert Order(x, (x, 0)) + Order(x, (x, oo)) == Order(x, (x, oo)) + Order(x, (x, 0))
    assert Order(Order(x, (x, oo))) == Order(x, (x, oo))

    # not supported (yet)
    raises(NotImplementedError, lambda: Order(x, (x, 0))*Order(x, (x, oo)))
    raises(NotImplementedError, lambda: Order(x, (x, oo))*Order(x, (x, 0)))
    raises(NotImplementedError, lambda: Order(Order(x, (x, oo)), y))
    raises(NotImplementedError, lambda: Order(Order(x), (x, oo)))


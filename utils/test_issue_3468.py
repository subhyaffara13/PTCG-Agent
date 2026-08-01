
def test_issue_3468():
    y = Symbol('y', negative=True)
    z = Symbol('z', complex=True)

    # check that Order does not modify assumptions about symbols
    Order(x)
    Order(y)
    Order(z)

    assert x.is_positive is None
    assert y.is_positive is False
    assert z.is_positive is None


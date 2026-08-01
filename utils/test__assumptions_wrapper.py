
def test_AssumptionsWrapper():
    x = Symbol('x', positive=True)
    y = Symbol('y')
    assert AssumptionsWrapper(x).is_positive
    assert AssumptionsWrapper(y).is_positive is None
    assert AssumptionsWrapper(y, Q.positive(y)).is_positive


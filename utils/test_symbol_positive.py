
def test_symbol_positive():
    x = Symbol('x', positive=True)
    assert x.is_positive is True
    assert x.is_nonpositive is False
    assert x.is_negative is False
    assert x.is_nonnegative is True
    assert x.is_zero is False
    assert x.is_nonzero is True


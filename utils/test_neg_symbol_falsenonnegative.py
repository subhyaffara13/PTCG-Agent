
def test_neg_symbol_falsenonnegative():
    x = -Symbol('x', nonnegative=False)
    assert x.is_positive is None
    assert x.is_nonpositive is False  # this currently returns None
    assert x.is_negative is False  # this currently returns None
    assert x.is_nonnegative is None
    assert x.is_zero is False  # this currently returns None
    assert x.is_nonzero is True  # this currently returns None



def test_neg_symbol_falsepositive():
    x = -Symbol('x', positive=False)
    assert x.is_positive is None
    assert x.is_nonpositive is None
    assert x.is_negative is False
    assert x.is_nonnegative is None
    assert x.is_zero is None
    assert x.is_nonzero is None


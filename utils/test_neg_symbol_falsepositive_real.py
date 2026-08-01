
def test_neg_symbol_falsepositive_real():
    x = -Symbol('x', positive=False, real=True)
    assert x.is_positive is None
    assert x.is_nonpositive is None
    assert x.is_negative is False
    assert x.is_nonnegative is True
    assert x.is_zero is None
    assert x.is_nonzero is None


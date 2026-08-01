
def test_symbol_falsenonnegative_real():
    x = Symbol('x', nonnegative=False, real=True)
    assert x.is_positive is False
    assert x.is_nonpositive is True
    assert x.is_negative is True
    assert x.is_nonnegative is False
    assert x.is_zero is False
    assert x.is_nonzero is True


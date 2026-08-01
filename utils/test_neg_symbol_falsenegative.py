
def test_neg_symbol_falsenegative():
    # To test pull request 9379
    # Explicit handling of arg.is_negative=False was added to Mul._eval_is_positive
    x = -Symbol('x', negative=False)
    assert x.is_positive is False  # This was None before
    assert x.is_nonpositive is None
    assert x.is_negative is None
    assert x.is_nonnegative is None
    assert x.is_zero is None
    assert x.is_nonzero is None


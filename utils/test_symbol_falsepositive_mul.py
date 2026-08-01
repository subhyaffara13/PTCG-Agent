
def test_symbol_falsepositive_mul():
    # To test pull request 9379
    # Explicit handling of arg.is_positive=False was added to Mul._eval_is_positive
    x = 2*Symbol('x', positive=False)
    assert x.is_positive is False  # This was None before
    assert x.is_nonpositive is None
    assert x.is_negative is None
    assert x.is_nonnegative is None
    assert x.is_zero is None
    assert x.is_nonzero is None


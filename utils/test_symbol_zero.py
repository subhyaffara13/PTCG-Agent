
def test_symbol_zero():
    x = Symbol('x', zero=True)
    assert x.is_positive is False
    assert x.is_nonpositive
    assert x.is_negative is False
    assert x.is_nonnegative
    assert x.is_zero is True
    # TODO Change to x.is_nonzero is None
    # See https://github.com/sympy/sympy/pull/9583
    assert x.is_nonzero is False
    assert x.is_finite is True


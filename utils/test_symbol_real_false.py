
def test_symbol_real_false():
    # issue 3848
    a = Symbol('a', real=False)

    assert a.is_real is False
    assert a.is_integer is False
    assert a.is_zero is False

    assert a.is_negative is False
    assert a.is_positive is False
    assert a.is_nonnegative is False
    assert a.is_nonpositive is False
    assert a.is_nonzero is False

    assert a.is_extended_negative is None
    assert a.is_extended_positive is None
    assert a.is_extended_nonnegative is None
    assert a.is_extended_nonpositive is None
    assert a.is_extended_nonzero is None


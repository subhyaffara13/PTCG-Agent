
def test_Add_is_pos_neg():
    # these cover lines not covered by the rest of tests in core
    n = Symbol('n', extended_negative=True, infinite=True)
    nn = Symbol('n', extended_nonnegative=True, infinite=True)
    np = Symbol('n', extended_nonpositive=True, infinite=True)
    p = Symbol('p', extended_positive=True, infinite=True)
    r = Dummy(extended_real=True, finite=False)
    x = Symbol('x')
    xf = Symbol('xf', finite=True)
    assert (n + p).is_extended_positive is None
    assert (n + x).is_extended_positive is None
    assert (p + x).is_extended_positive is None
    assert (n + p).is_extended_negative is None
    assert (n + x).is_extended_negative is None
    assert (p + x).is_extended_negative is None

    assert (n + xf).is_extended_positive is False
    assert (p + xf).is_extended_positive is True
    assert (n + xf).is_extended_negative is True
    assert (p + xf).is_extended_negative is False

    assert (x - S.Infinity).is_extended_negative is None  # issue 7798
    # issue 8046, 16.2
    assert (p + nn).is_extended_positive
    assert (n + np).is_extended_negative
    assert (p + r).is_extended_positive is None


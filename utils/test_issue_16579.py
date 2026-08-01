
def test_issue_16579():
    # extended_real -> finite | infinite
    x = Symbol('x', extended_real=True, infinite=False)
    y = Symbol('y', extended_real=True, finite=False)
    assert x.is_finite is True
    assert y.is_infinite is True

    # With PR 16978, complex now implies finite
    c = Symbol('c', complex=True)
    assert c.is_finite is True
    raises(InconsistentAssumptions, lambda: Dummy(complex=True, finite=False))

    # Now infinite == !finite
    nf = Symbol('nf', finite=False)
    assert nf.is_infinite is True


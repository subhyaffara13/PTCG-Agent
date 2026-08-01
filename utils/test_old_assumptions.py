
def test_old_assumptions():
    # test unhandled old assumptions
    w = symbols("w")
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", rational=False, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", odd=True, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", even=True, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", prime=True, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", composite=True, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", integer=True, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))
    w = symbols("w", integer=False, real=True)
    raises(UnhandledInput, lambda: lra_satask(Q.lt(w, 2) & Q.gt(w, 3)))

    # test handled
    w = symbols("w", positive=True, real=True)
    assert lra_satask(Q.le(w, 0)) is False
    assert lra_satask(Q.gt(w, 0)) is True
    w = symbols("w", negative=True, real=True)
    assert lra_satask(Q.lt(w, 0)) is True
    assert lra_satask(Q.ge(w, 0)) is False
    w = symbols("w", zero=True, real=True)
    assert lra_satask(Q.eq(w, 0)) is True
    assert lra_satask(Q.ne(w, 0)) is False
    w = symbols("w", nonzero=True, real=True)
    assert lra_satask(Q.ne(w, 0)) is True
    assert lra_satask(Q.eq(w, 1)) is None
    w = symbols("w", nonpositive=True, real=True)
    assert lra_satask(Q.le(w, 0)) is True
    assert lra_satask(Q.gt(w, 0)) is False
    w = symbols("w", nonnegative=True, real=True)
    assert lra_satask(Q.ge(w, 0)) is True
    assert lra_satask(Q.lt(w, 0)) is False



def test_Pow_is_finite():
    xe = Symbol('xe', extended_real=True)
    xr = Symbol('xr', real=True)
    p = Symbol('p', positive=True)
    n = Symbol('n', negative=True)
    i = Symbol('i', integer=True)

    assert (xe**2).is_finite is None  # xe could be oo
    assert (xr**2).is_finite is True

    assert (xe**xe).is_finite is None
    assert (xr**xe).is_finite is None
    assert (xe**xr).is_finite is None
    # FIXME: The line below should be True rather than None
    # assert (xr**xr).is_finite is True
    assert (xr**xr).is_finite is None

    assert (p**xe).is_finite is None
    assert (p**xr).is_finite is True

    assert (n**xe).is_finite is None
    assert (n**xr).is_finite is True

    assert (sin(xe)**2).is_finite is True
    assert (sin(xr)**2).is_finite is True

    assert (sin(xe)**xe).is_finite is None  # xe, xr could be -pi
    assert (sin(xr)**xr).is_finite is None

    # FIXME: Should the line below be True rather than None?
    assert (sin(xe)**exp(xe)).is_finite is None
    assert (sin(xr)**exp(xr)).is_finite is True

    assert (1/sin(xe)).is_finite is None  # if zero, no, otherwise yes
    assert (1/sin(xr)).is_finite is None

    assert (1/exp(xe)).is_finite is None  # xe could be -oo
    assert (1/exp(xr)).is_finite is True

    assert (1/S.Pi).is_finite is True

    assert (1/(i-1)).is_finite is None


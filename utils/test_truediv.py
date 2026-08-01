
def test_truediv():
    assert 1/2 != 0
    assert Rational(1)/2 != 0


def test_truediv(Poly):
    # true division is valid only if the denominator is a Number and
    # not a python bool.
    p1 = Poly([1, 2, 3])
    p2 = p1 * 5

    for stype in np.ScalarType:
        if (
            not issubclass(stype, Number)
            or issubclass(stype, bool)
            or issubclass(stype, np.timedelta64)
        ):
            continue
        s = stype(5)
        assert_poly_almost_equal(op.truediv(p2, s), p1)
        assert_raises(TypeError, op.truediv, s, p2)
    for stype in (int, float):
        s = stype(5)
        assert_poly_almost_equal(op.truediv(p2, s), p1)
        assert_raises(TypeError, op.truediv, s, p2)
    for stype in [complex]:
        s = stype(5, 0)
        assert_poly_almost_equal(op.truediv(p2, s), p1)
        assert_raises(TypeError, op.truediv, s, p2)
    for stype in [np.timedelta64]:
        s = stype(5, 'D')
        with pytest.warns(
            DeprecationWarning,
            match="The 'generic' unit for NumPy timedelta is deprecated",
        ):
            assert_poly_almost_equal(op.truediv(p2, s), p1)
        assert_raises(TypeError, op.truediv, s, p2)
    for s in [(), [], {}, False, np.array([1])]:
        assert_raises(TypeError, op.truediv, p2, s)
        assert_raises(TypeError, op.truediv, s, p2)
    for ptype in classes:
        assert_raises(TypeError, op.truediv, p2, ptype(1))



def test_scalar_matches_array_op_with_pyscalar(op, sctype, other_type, rop):
    # Check that the ufunc path matches by coercing to an array explicitly
    val1 = sctype(2)
    val2 = other_type(2)

    if rop:
        _op = op
        op = lambda x, y: _op(y, x)

    try:
        res = op(val1, val2)
    except TypeError:
        try:
            expected = op(np.asarray(val1), val2)
            raise AssertionError("ufunc didn't raise.")
        except TypeError:
            return
    else:
        expected = op(np.asarray(val1), val2)

    # Note that we only check dtype equivalency, as ufuncs may pick the lower
    # dtype if they are equivalent.
    assert res == expected
    if isinstance(val1, float) and other_type is complex and rop:
        # Python complex accepts float subclasses, so we don't get a chance
        # and the result may be a Python complex (thus, the `np.array()``)
        assert np.array(res).dtype == expected.dtype
    else:
        assert res.dtype == expected.dtype


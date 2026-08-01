
def test_longdouble_with_arrlike(sctype, op):
    # As of NumPy 2.1, longdouble behaves like other types and can coerce
    # e.g. lists.  (Not necessarily better, but consistent.)
    assert_array_equal(op(sctype(3), [1, 2]), op(3, np.array([1, 2])))
    assert_array_equal(op([1, 2], sctype(3)), op(np.array([1, 2]), 3))


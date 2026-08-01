
def test_squeeze_element():
    a = np.zeros((1,3))
    assert_array_equal(np.squeeze(a), squeeze_element(a))
    # 0-D output from squeeze gives scalar
    sq_int = squeeze_element(np.zeros((1,1), dtype=float))
    assert_(isinstance(sq_int, float))
    # Unless it's a structured array
    sq_sa = squeeze_element(np.zeros((1,1),dtype=[('f1', 'f')]))
    assert_(isinstance(sq_sa, np.ndarray))
    # Squeezing empty arrays maintain their dtypes.
    sq_empty = squeeze_element(np.empty(0, np.uint8))
    assert sq_empty.dtype == np.uint8


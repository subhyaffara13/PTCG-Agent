
def test_logical_array():
    # The roundtrip test doesn't verify that we load the data up with the
    # correct (bool) dtype
    with open(pjoin(test_data_path, 'testbool_8_WIN64.mat'), 'rb') as fobj:
        rdr = MatFile5Reader(fobj, mat_dtype=True)
        d = rdr.get_variables()
    x = np.array([[True], [False]], dtype=np.bool_)
    assert_array_equal(d['testbools'], x)
    assert_equal(d['testbools'].dtype, x.dtype)


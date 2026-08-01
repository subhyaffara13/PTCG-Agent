
def test_empty_string():
    # make sure reading empty string does not raise error
    estring_fname = pjoin(test_data_path, 'single_empty_string.mat')
    fp = open(estring_fname, 'rb')
    rdr = MatFile5Reader(fp)
    d = rdr.get_variables()
    fp.close()
    assert_array_equal(d['a'], np.array([], dtype='U1'))
    # Empty string round trip. Matlab cannot distinguish
    # between a string array that is empty, and a string array
    # containing a single empty string, because it stores strings as
    # arrays of char. There is no way of having an array of char that
    # is not empty, but contains an empty string.
    stream = BytesIO()
    savemat(stream, {'a': np.array([''])})
    rdr = MatFile5Reader(stream)
    d = rdr.get_variables()
    assert_array_equal(d['a'], np.array([], dtype='U1'))
    stream.truncate(0)
    stream.seek(0)
    savemat(stream, {'a': np.array([], dtype='U1')})
    rdr = MatFile5Reader(stream)
    d = rdr.get_variables()
    assert_array_equal(d['a'], np.array([], dtype='U1'))
    stream.close()


def test_empty_string():
    # Empty strings are unfortunately often converted to S1 and we need to
    # make sure we are filling the S1 and not the (possibly) detected S0
    # result.  This should likely just return S0 and if not maybe the decision
    # to return S1 should be moved.
    res = np.array([""] * 10, dtype="S")
    assert_array_equal(res, np.array("\0", "S1"))
    assert res.dtype == "S1"

    arr = np.array([""] * 10, dtype=object)

    res = arr.astype("S")
    assert_array_equal(res, b"")
    assert res.dtype == "S1"

    res = np.array(arr, dtype="S")
    assert_array_equal(res, b"")
    # TODO: This is arguably weird/wrong, but seems old:
    assert res.dtype == f"S{np.dtype('O').itemsize}"

    res = np.array([[""] * 10, arr], dtype="S")
    assert_array_equal(res, b"")
    assert res.shape == (2, 10)
    assert res.dtype == "S1"


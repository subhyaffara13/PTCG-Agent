
def test_write_opposite_endian():
    # We don't support writing opposite endian .mat files, but we need to behave
    # correctly if the user supplies an other-endian NumPy array to write out.
    float_arr = np.array([[2., 3.],
                          [3., 4.]])
    int_arr = np.arange(6).reshape((2, 3))
    uni_arr = np.array(['hello', 'world'], dtype='U')
    stream = BytesIO()
    savemat(stream, {
        'floats': float_arr.byteswap().view(float_arr.dtype.newbyteorder()),
        'ints': int_arr.byteswap().view(int_arr.dtype.newbyteorder()),
        'uni_arr': uni_arr.byteswap().view(uni_arr.dtype.newbyteorder()),
    })
    rdr = MatFile5Reader(stream)
    d = rdr.get_variables()
    assert_array_equal(d['floats'], float_arr)
    assert_array_equal(d['ints'], int_arr)
    assert_array_equal(d['uni_arr'], uni_arr)
    stream.close()



def test_read_opts():
    # tests if read is seeing option sets, at initialization and after
    # initialization
    arr = np.arange(6).reshape(1,6)
    stream = BytesIO()
    savemat(stream, {'a': arr})
    rdr = MatFile5Reader(stream)
    back_dict = rdr.get_variables()
    rarr = back_dict['a']
    assert_array_equal(rarr, arr)
    rdr = MatFile5Reader(stream, squeeze_me=True)
    assert_array_equal(rdr.get_variables()['a'], arr.reshape((6,)))
    rdr.squeeze_me = False
    assert_array_equal(rarr, arr)
    rdr = MatFile5Reader(stream, byte_order=boc.native_code)
    assert_array_equal(rdr.get_variables()['a'], arr)
    # inverted byte code leads to error on read because of swapped
    # header etc.
    rdr = MatFile5Reader(stream, byte_order=boc.swapped_code)
    assert_raises(Exception, rdr.get_variables)
    rdr.byte_order = boc.native_code
    assert_array_equal(rdr.get_variables()['a'], arr)
    arr = np.array(['a string'])
    stream.truncate(0)
    stream.seek(0)
    savemat(stream, {'a': arr})
    rdr = MatFile5Reader(stream)
    assert_array_equal(rdr.get_variables()['a'], arr)
    rdr = MatFile5Reader(stream, chars_as_strings=False)
    carr = np.atleast_2d(np.array(list(arr.item()), dtype='U1'))
    assert_array_equal(rdr.get_variables()['a'], carr)
    rdr.chars_as_strings = True
    assert_array_equal(rdr.get_variables()['a'], arr)


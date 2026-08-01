
def test_iter_buffering_string():
    # Safe casting disallows shrinking strings
    a = np.array(['abc', 'a', 'abcd'], dtype=np.bytes_)
    assert_equal(a.dtype, np.dtype('S4'))
    assert_raises(TypeError, nditer, a, ['buffered'], ['readonly'],
                  op_dtypes='S2')
    i = nditer(a, ['buffered'], ['readonly'], op_dtypes='S6')
    assert_equal(i[0], b'abc')
    assert_equal(i[0].dtype, np.dtype('S6'))

    a = np.array(['abc', 'a', 'abcd'], dtype=np.str_)
    assert_equal(a.dtype, np.dtype('U4'))
    assert_raises(TypeError, nditer, a, ['buffered'], ['readonly'],
                    op_dtypes='U2')
    i = nditer(a, ['buffered'], ['readonly'], op_dtypes='U6')
    assert_equal(i[0], 'abc')
    assert_equal(i[0].dtype, np.dtype('U6'))


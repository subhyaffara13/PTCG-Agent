
def test_str_round():
    # from report by Angus McMorland on mailing list 3 May 2010
    stream = BytesIO()
    in_arr = np.array(['Hello', 'Foob'])
    out_arr = np.array(['Hello', 'Foob '])
    savemat(stream, dict(a=in_arr))
    res = loadmat(stream)
    # resulted in ['HloolFoa', 'elWrdobr']
    assert_array_equal(res['a'], out_arr)
    stream.truncate(0)
    stream.seek(0)
    # Make Fortran ordered version of string
    in_str = in_arr.tobytes(order='F')
    in_from_str = np.ndarray(shape=a.shape,
                             dtype=in_arr.dtype,
                             order='F',
                             buffer=in_str)
    savemat(stream, dict(a=in_from_str))
    assert_array_equal(res['a'], out_arr)
    # unicode save did lead to buffer too small error
    stream.truncate(0)
    stream.seek(0)
    in_arr_u = in_arr.astype('U')
    out_arr_u = out_arr.astype('U')
    savemat(stream, {'a': in_arr_u})
    res = loadmat(stream)
    assert_array_equal(res['a'], out_arr_u)


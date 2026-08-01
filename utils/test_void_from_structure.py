
def test_void_from_structure():
    dtype = np.dtype([('s', [('f', 'f8'), ('u', 'U1')]), ('i', 'i2')])
    data = np.array(((1., 'a'), 2), dtype=dtype)
    res = np.void(data[()], dtype=dtype)
    assert type(res) is np.void
    assert res.dtype == dtype
    assert res == data[()]


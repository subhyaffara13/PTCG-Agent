
def test_round_types():
    # Check that saving, loading preserves dtype in most cases
    arr = np.arange(10)
    stream = BytesIO()
    for dts in ('f8','f4','i8','i4','i2','i1',
                'u8','u4','u2','u1','c16','c8'):
        stream.truncate(0)
        stream.seek(0)  # needed for BytesIO in Python 3
        savemat(stream, {'arr': arr.astype(dts)})
        vars = loadmat(stream)
        assert_equal(np.dtype(dts), vars['arr'].dtype)


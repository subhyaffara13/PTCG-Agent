
def test_signaling_nan_exceptions():
    with assert_no_warnings():
        a = np.ndarray(shape=(), dtype='float32', buffer=b'\x00\xe0\xbf\xff')
        np.isnan(a)


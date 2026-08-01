
def test_bandwidth_dtypes():
    n = 5
    for dt in BANDWIDTH_DTYPES:
        _ = bandwidth(np.zeros([n, n], dtype=dt))

    unsupported_dtypes = [np.float16, np.longdouble, np.clongdouble,
                          np.bytes_, np.str_, np.void, np.object_,
                          np.datetime64, np.timedelta64]
    for dt in unsupported_dtypes:
        raises(TypeError, bandwidth, np.zeros([n, n], dtype=dt))



def test_nanmean_overflow(disable_bottleneck, val, using_python_scalars):
    # GH 10155
    # In the previous implementation mean can overflow for int dtypes, it
    # is now consistent with numpy

    ser = Series(val, index=range(500), dtype=np.int64)
    result = ser.mean()
    assert result == val
    if using_python_scalars:
        assert type(result) == float
    else:
        np_result = ser.values.mean()
        assert result == np_result
        assert result.dtype == np.float64


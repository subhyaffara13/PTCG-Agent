
def test_cast_1d_array_like_from_timestamp(fixed_now_ts):
    # check we dont lose nanoseconds
    ts = fixed_now_ts + Timedelta(1)
    res = construct_1d_arraylike_from_scalar(ts, 2, np.dtype("M8[ns]"))
    assert res[0] == ts


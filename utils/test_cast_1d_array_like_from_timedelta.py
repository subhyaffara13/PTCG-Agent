
def test_cast_1d_array_like_from_timedelta():
    # check we dont lose nanoseconds
    td = Timedelta(1)
    res = construct_1d_arraylike_from_scalar(td, 2, np.dtype("m8[ns]"))
    assert res[0] == td


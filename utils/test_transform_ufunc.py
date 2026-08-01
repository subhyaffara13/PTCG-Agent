
def test_transform_ufunc(axis, float_frame, frame_or_series):
    # GH 35964
    obj = unpack_obj(float_frame, frame_or_series, axis)

    with np.errstate(all="ignore"):
        f_sqrt = np.sqrt(obj)

    # ufunc
    result = obj.transform(np.sqrt, axis=axis)
    expected = f_sqrt
    tm.assert_equal(result, expected)


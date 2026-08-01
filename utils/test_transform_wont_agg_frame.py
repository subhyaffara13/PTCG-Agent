
def test_transform_wont_agg_frame(axis, float_frame, func):
    # GH 35964
    # cannot both transform and agg
    msg = "Function did not transform"
    with pytest.raises(ValueError, match=msg):
        float_frame.transform(func, axis=axis)


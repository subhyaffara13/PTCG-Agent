
def test_transform_and_agg_err_agg(axis, float_frame):
    # cannot both transform and agg
    msg = "cannot combine transform and aggregation operations"
    with pytest.raises(ValueError, match=msg):
        with np.errstate(all="ignore"):
            float_frame.agg(["max", "sqrt"], axis=axis)


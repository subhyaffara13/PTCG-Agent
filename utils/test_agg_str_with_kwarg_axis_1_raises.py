
def test_agg_str_with_kwarg_axis_1_raises(df, reduction_func):
    gb = df.groupby(level=0)
    msg = f"Operation {reduction_func} does not support axis=1"
    with pytest.raises(ValueError, match=msg):
        gb.agg(reduction_func, axis=1)


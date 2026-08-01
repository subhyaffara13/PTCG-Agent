
def test_named_agg_reduce_axis1_raises(float_frame):
    name1, name2 = float_frame.axes[0].unique()[:2].sort_values()
    msg = "Named aggregation is not supported when axis=1."
    for axis in [1, "columns"]:
        with pytest.raises(NotImplementedError, match=msg):
            float_frame.agg(row1=(name1, "sum"), row2=(name2, "max"), axis=axis)


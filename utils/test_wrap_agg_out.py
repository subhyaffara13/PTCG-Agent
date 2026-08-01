
def test_wrap_agg_out(three_group):
    grouped = three_group.groupby(["A", "B"])

    def func(ser):
        if ser.dtype in (object, "string"):
            raise TypeError("Test error message")
        return ser.sum()

    with pytest.raises(TypeError, match="Test error message"):
        grouped.aggregate(func)
    result = grouped[["D", "E", "F"]].aggregate(func)
    exp_grouped = three_group.loc[:, ["A", "B", "D", "E", "F"]]
    expected = exp_grouped.groupby(["A", "B"]).aggregate(func)
    tm.assert_frame_equal(result, expected)


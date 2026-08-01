
def test_aggregate_str_func(tsframe, groupbyfunc):
    grouped = tsframe.groupby(groupbyfunc)

    # single series
    result = grouped["A"].agg("std")
    expected = grouped["A"].std()
    tm.assert_series_equal(result, expected)

    # group frame by function name
    result = grouped.aggregate("var")
    expected = grouped.var()
    tm.assert_frame_equal(result, expected)

    # group frame by function dict
    result = grouped.agg({"A": "var", "B": "std", "C": "mean", "D": "sem"})
    expected = DataFrame(
        {
            "A": grouped["A"].var(),
            "B": grouped["B"].std(),
            "C": grouped["C"].mean(),
            "D": grouped["D"].sem(),
        }
    )
    tm.assert_frame_equal(result, expected)


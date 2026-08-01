
def test_apply_is_unchanged_when_other_methods_are_called_first(reduction_func):
    # GH #34656
    # GH #34271
    df = DataFrame(
        {
            "a": [99, 99, 99, 88, 88, 88],
            "b": [1, 2, 3, 4, 5, 6],
            "c": [10, 20, 30, 40, 50, 60],
        }
    )

    expected = DataFrame(
        {"b": [15, 6], "c": [150, 60]},
        index=Index([88, 99], name="a"),
    )

    # Check output when no other methods are called before .apply()
    grp = df.groupby(by="a")
    result = grp.apply(np.sum, axis=0)
    tm.assert_frame_equal(result, expected)

    # Check output when another method is called before .apply()
    grp = df.groupby(by="a")
    args = get_groupby_method_args(reduction_func, df)
    if reduction_func == "corrwith":
        warn = Pandas4Warning
        msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        msg = ""
    with tm.assert_produces_warning(warn, match=msg):
        _ = getattr(grp, reduction_func)(*args)
    result = grp.apply(np.sum, axis=0)
    tm.assert_frame_equal(result, expected)


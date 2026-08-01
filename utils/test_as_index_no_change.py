
def test_as_index_no_change(keys, df, groupby_func):
    # GH#49834 - as_index should have no impact on DataFrameGroupBy.transform
    if keys == "A":
        # Column B is string dtype; will fail on some ops
        df = df.drop(columns="B")
    args = get_groupby_method_args(groupby_func, df)
    gb_as_index_true = df.groupby(keys, as_index=True)
    gb_as_index_false = df.groupby(keys, as_index=False)
    if groupby_func == "corrwith":
        warn = Pandas4Warning
        msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        msg = ""
    with tm.assert_produces_warning(warn, match=msg):
        result = gb_as_index_true.transform(groupby_func, *args)
    with tm.assert_produces_warning(warn, match=msg):
        expected = gb_as_index_false.transform(groupby_func, *args)
    tm.assert_equal(result, expected)



def test_multiindex_group_all_columns_when_empty(groupby_func):
    # GH 32464
    df = DataFrame({"a": [], "b": [], "c": []}).set_index(["a", "b", "c"])
    gb = df.groupby(["a", "b", "c"], group_keys=True)
    method = getattr(gb, groupby_func)
    args = get_groupby_method_args(groupby_func, df)
    if groupby_func == "corrwith":
        warn = Pandas4Warning
        warn_msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        warn_msg = ""
    with tm.assert_produces_warning(warn, match=warn_msg):
        result = method(*args).index
    expected = df.index
    tm.assert_index_equal(result, expected)


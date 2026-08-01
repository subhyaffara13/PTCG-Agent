
def test_dup_labels_output_shape(groupby_func, idx):
    if groupby_func in {"size", "ngroup", "cumcount"}:
        pytest.skip(f"Not applicable for {groupby_func}")

    df = DataFrame([[1, 1]], columns=idx)
    grp_by = df.groupby([0])

    args = get_groupby_method_args(groupby_func, df)
    if groupby_func == "corrwith":
        warn = Pandas4Warning
        warn_msg = "DataFrameGroupBy.corrwith is deprecated"
    else:
        warn = None
        warn_msg = ""
    with tm.assert_produces_warning(warn, match=warn_msg):
        result = getattr(grp_by, groupby_func)(*args)

    assert result.shape == (1, 2)
    tm.assert_index_equal(result.columns, idx)


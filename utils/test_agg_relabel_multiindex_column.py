
def test_agg_relabel_multiindex_column(
    agg_col1, agg_col2, agg_col3, agg_result1, agg_result2, agg_result3
):
    # GH 29422, add tests for multiindex column cases
    df = DataFrame(
        {"group": ["a", "a", "b", "b"], "A": [0, 1, 2, 3], "B": [5, 6, 7, 8]}
    )
    df.columns = MultiIndex.from_tuples([("x", "group"), ("y", "A"), ("y", "B")])
    idx = Index(["a", "b"], name=("x", "group"))

    result = df.groupby(("x", "group")).agg(a_max=(("y", "A"), "max"))
    expected = DataFrame({"a_max": [1, 3]}, index=idx)
    tm.assert_frame_equal(result, expected)

    result = df.groupby(("x", "group")).agg(
        col_1=agg_col1, col_2=agg_col2, col_3=agg_col3
    )
    expected = DataFrame(
        {"col_1": agg_result1, "col_2": agg_result2, "col_3": agg_result3}, index=idx
    )
    tm.assert_frame_equal(result, expected)



def test_groupby_filtered_df_std():
    # GH 16174
    dicts = [
        {"filter_col": False, "groupby_col": True, "bool_col": True, "float_col": 10.5},
        {"filter_col": True, "groupby_col": True, "bool_col": True, "float_col": 20.5},
        {"filter_col": True, "groupby_col": True, "bool_col": True, "float_col": 30.5},
    ]
    df = DataFrame(dicts)

    df_filter = df[df["filter_col"] == True]  # noqa: E712
    dfgb = df_filter.groupby("groupby_col")
    result = dfgb.std()
    expected = DataFrame(
        [[0.0, 0.0, 7.071068]],
        columns=["filter_col", "bool_col", "float_col"],
        index=Index([True], name="groupby_col"),
    )
    tm.assert_frame_equal(result, expected)



def test_groupby_numeric_only_std_no_result(numeric_only):
    # GH 51080
    dicts_non_numeric = [{"a": "foo", "b": "bar"}, {"a": "car", "b": "dar"}]
    df = DataFrame(dicts_non_numeric, dtype=object)
    dfgb = df.groupby("a", as_index=False, sort=False)

    if numeric_only:
        result = dfgb.std(numeric_only=True)
        expected_df = DataFrame(["foo", "car"], columns=["a"])
        tm.assert_frame_equal(result, expected_df)
    else:
        with pytest.raises(
            ValueError, match="could not convert string to float: 'bar'"
        ):
            dfgb.std(numeric_only=numeric_only)


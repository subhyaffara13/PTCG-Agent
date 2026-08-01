
def test_compare_with_non_equal_nulls():
    # We want to make sure the relevant NaNs do not get dropped
    s1 = pd.Series(["a", "b", "c"])
    s2 = pd.Series(["x", "b", np.nan])

    result = s1.compare(s2, align_axis=0)

    indices = pd.MultiIndex.from_product([[0, 2], ["self", "other"]])
    expected = pd.Series(["a", "x", "c", np.nan], index=indices)
    tm.assert_series_equal(result, expected)


def test_compare_with_non_equal_nulls():
    # We want to make sure the relevant NaNs do not get dropped
    # even if the entire row or column are NaNs
    df = pd.DataFrame(
        {"col1": ["a", "b", "c"], "col2": [1.0, 2.0, np.nan], "col3": [1.0, 2.0, 3.0]},
        columns=["col1", "col2", "col3"],
    )
    df2 = df.copy()
    df2.loc[0, "col1"] = "c"
    df2.loc[2, "col3"] = np.nan

    result = df.compare(df2)

    indices = pd.Index([0, 2])
    columns = pd.MultiIndex.from_product([["col1", "col3"], ["self", "other"]])
    expected = pd.DataFrame(
        [["a", "c", np.nan, np.nan], [np.nan, np.nan, 3.0, np.nan]],
        index=indices,
        columns=columns,
    )
    tm.assert_frame_equal(result, expected)



def test_compare_with_equal_nulls():
    # We want to make sure two NaNs are considered the same
    # and dropped where applicable
    s1 = pd.Series(["a", "b", np.nan])
    s2 = pd.Series(["x", "b", np.nan])

    result = s1.compare(s2)
    expected = pd.DataFrame([["a", "x"]], columns=["self", "other"])
    tm.assert_frame_equal(result, expected)


def test_compare_with_equal_nulls():
    # We want to make sure two NaNs are considered the same
    # and dropped where applicable
    df = pd.DataFrame(
        {"col1": ["a", "b", "c"], "col2": [1.0, 2.0, np.nan], "col3": [1.0, 2.0, 3.0]},
        columns=["col1", "col2", "col3"],
    )
    df2 = df.copy()
    df2.loc[0, "col1"] = "c"

    result = df.compare(df2)
    indices = pd.Index([0])
    columns = pd.MultiIndex.from_product([["col1"], ["self", "other"]])
    expected = pd.DataFrame([["a", "c"]], index=indices, columns=columns)
    tm.assert_frame_equal(result, expected)


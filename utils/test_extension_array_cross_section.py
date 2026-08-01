
def test_extension_array_cross_section():
    # A cross-section of a homogeneous EA should be an EA
    df = DataFrame(
        {
            "A": pd.array([1, 2], dtype="Int64"),
            "B": pd.array([3, 4], dtype="Int64"),
        },
        index=["a", "b"],
    )
    expected = Series(pd.array([1, 3], dtype="Int64"), index=["A", "B"], name="a")
    result = df.loc["a"]
    tm.assert_series_equal(result, expected)

    result = df.iloc[0]
    tm.assert_series_equal(result, expected)


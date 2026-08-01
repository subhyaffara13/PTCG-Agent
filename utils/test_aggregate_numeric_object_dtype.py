
def test_aggregate_numeric_object_dtype():
    # https://github.com/pandas-dev/pandas/issues/39329
    # simplified case: multiple object columns where one is all-NaN
    # -> gets split as the all-NaN is inferred as float
    df = DataFrame(
        {"key": ["A", "A", "B", "B"], "col1": list("abcd"), "col2": [np.nan] * 4},
    ).astype(object)
    result = df.groupby("key").min()
    expected = (
        DataFrame(
            {"key": ["A", "B"], "col1": ["a", "c"], "col2": [np.nan, np.nan]},
        )
        .set_index("key")
        .astype(object)
    )
    tm.assert_frame_equal(result, expected)

    # same but with numbers
    df = DataFrame(
        {"key": ["A", "A", "B", "B"], "col1": list("abcd"), "col2": range(4)},
    ).astype(object)
    result = df.groupby("key").min()
    expected = (
        DataFrame({"key": ["A", "B"], "col1": ["a", "c"], "col2": [0, 2]})
        .set_index("key")
        .astype(object)
    )
    tm.assert_frame_equal(result, expected)


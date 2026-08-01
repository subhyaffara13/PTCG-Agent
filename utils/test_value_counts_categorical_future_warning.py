
def test_value_counts_categorical_future_warning():
    # GH#54775
    df = pd.DataFrame({"a": [1, 2, 3]}, dtype="category")
    result = df.value_counts()
    expected = pd.Series(
        1,
        index=pd.MultiIndex.from_arrays(
            [pd.Index([1, 2, 3], name="a", dtype="category")]
        ),
        name="count",
    )
    tm.assert_series_equal(result, expected)


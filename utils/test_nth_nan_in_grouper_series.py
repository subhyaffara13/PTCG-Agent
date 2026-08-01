
def test_nth_nan_in_grouper_series(dropna):
    # GH 26454
    df = DataFrame(
        {
            "a": [np.nan, "a", np.nan, "b", np.nan],
            "b": [0, 2, 4, 6, 8],
        }
    )
    result = df.groupby("a")["b"].nth(0, dropna=dropna)
    expected = df["b"].iloc[[1, 3]]

    tm.assert_series_equal(result, expected)



def test_observed_nth():
    # GH 26385
    cat = Categorical(["a", np.nan, np.nan], categories=["a", "b", "c"])
    ser = Series([1, 2, 3])
    df = DataFrame({"cat": cat, "ser": ser})

    result = df.groupby("cat", observed=False)["ser"].nth(0)
    expected = df["ser"].iloc[[0]]
    tm.assert_series_equal(result, expected)


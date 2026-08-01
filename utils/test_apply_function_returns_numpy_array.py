
def test_apply_function_returns_numpy_array():
    # GH 31605
    def fct(group):
        return group["B"].values.flatten()

    df = DataFrame({"A": ["a", "a", "b", "none"], "B": [1, 2, 3, np.nan]})

    result = df.groupby("A").apply(fct)
    expected = Series(
        [[1.0, 2.0], [3.0], [np.nan]], index=Index(["a", "b", "none"], name="A")
    )
    tm.assert_series_equal(result, expected)


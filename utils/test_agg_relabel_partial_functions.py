
def test_agg_relabel_partial_functions():
    # GH 26513, test on partial, functools or more complex cases
    df = pd.DataFrame({"A": [1, 2, 1, 2], "B": [1, 2, 3, 4], "C": [3, 4, 5, 6]})
    result = df.agg(foo=("A", np.mean), bar=("A", "mean"), cat=("A", min))
    expected = pd.DataFrame(
        {"A": [1.5, 1.5, 1.0]}, index=pd.Index(["foo", "bar", "cat"])
    )
    tm.assert_frame_equal(result, expected)

    result = df.agg(
        foo=("A", min),
        bar=("B", np.min),
        cat=("B", max),
        dat=("C", "min"),
        f=("B", np.sum),
        kk=("B", lambda x: min(x)),
    )
    expected = pd.DataFrame(
        {
            "A": [1.0, np.nan, np.nan, np.nan, np.nan, np.nan],
            "B": [np.nan, 1.0, 4.0, np.nan, 10.0, 1.0],
            "C": [np.nan, np.nan, np.nan, 3.0, np.nan, np.nan],
        },
        index=pd.Index(["foo", "bar", "cat", "dat", "f", "kk"]),
    )
    tm.assert_frame_equal(result, expected)


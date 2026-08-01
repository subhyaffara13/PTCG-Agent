
def test_agg_namedtuple():
    # GH 26513
    df = pd.DataFrame({"A": [0, 1], "B": [1, 2]})
    result = df.agg(
        foo=pd.NamedAgg("B", "sum"),
        bar=pd.NamedAgg("B", "min"),
        cat=pd.NamedAgg(column="B", aggfunc="count"),
        fft=pd.NamedAgg("B", aggfunc="max"),
    )

    expected = pd.DataFrame(
        {"B": [3, 1, 2, 2]}, index=pd.Index(["foo", "bar", "cat", "fft"])
    )
    tm.assert_frame_equal(result, expected)

    result = df.agg(
        foo=pd.NamedAgg("A", "min"),
        bar=pd.NamedAgg(column="B", aggfunc="max"),
        cat=pd.NamedAgg(column="A", aggfunc="max"),
    )
    expected = pd.DataFrame(
        {"A": [0.0, np.nan, 1.0], "B": [np.nan, 2.0, np.nan]},
        index=pd.Index(["foo", "bar", "cat"]),
    )
    tm.assert_frame_equal(result, expected)


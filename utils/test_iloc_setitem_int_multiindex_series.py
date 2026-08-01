
def test_iloc_setitem_int_multiindex_series(data, indexes, values, expected_k):
    # GH17148
    df = DataFrame(data=data, columns=["i", "j", "k"])
    df = df.set_index(["i", "j"])

    series = df.k.copy()
    for i, v in zip(indexes, values):
        series.iloc[i] += v

    df["k"] = expected_k
    expected = df.k
    tm.assert_series_equal(series, expected)


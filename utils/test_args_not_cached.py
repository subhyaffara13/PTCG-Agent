
def test_args_not_cached():
    # GH 41647
    pytest.importorskip("numba")

    def sum_last(values, index, n):
        return values[-n:].sum()

    df = DataFrame({"id": [0, 0, 1, 1], "x": [1, 1, 1, 1]})
    grouped_x = df.groupby("id")["x"]
    result = grouped_x.agg(sum_last, 1, engine="numba")
    expected = Series([1.0] * 2, name="x", index=Index([0, 1], name="id"))
    tm.assert_series_equal(result, expected)

    result = grouped_x.agg(sum_last, 2, engine="numba")
    expected = Series([2.0] * 2, name="x", index=Index([0, 1], name="id"))
    tm.assert_series_equal(result, expected)


def test_args_not_cached():
    # GH 41647
    pytest.importorskip("numba")

    def sum_last(values, index, n):
        return values[-n:].sum()

    df = DataFrame({"id": [0, 0, 1, 1], "x": [1, 1, 1, 1]})
    grouped_x = df.groupby("id")["x"]
    result = grouped_x.transform(sum_last, 1, engine="numba")
    expected = Series([1.0] * 4, name="x")
    tm.assert_series_equal(result, expected)

    result = grouped_x.transform(sum_last, 2, engine="numba")
    expected = Series([2.0] * 4, name="x")
    tm.assert_series_equal(result, expected)


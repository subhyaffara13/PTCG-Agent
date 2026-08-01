
def test_index_order_consistency_preserved():
    # GH 57069
    pytest.importorskip("numba")

    def f(values, index):
        return values

    df = DataFrame(
        {"vals": [0.0, 1.0, 2.0, 3.0], "group": [0, 1, 0, 1]}, index=range(3, -1, -1)
    )
    result = df.groupby("group")["vals"].transform(f, engine="numba")
    expected = Series([0.0, 1.0, 2.0, 3.0], index=range(3, -1, -1), name="vals")
    tm.assert_series_equal(result, expected)


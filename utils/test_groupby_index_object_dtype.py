
def test_groupby_index_object_dtype():
    # GH 40014
    df = DataFrame({"c0": ["x", "x", "x"], "c1": ["x", "x", "y"], "p": [0, 1, 2]})
    df.index = df.index.astype("O")
    grouped = df.groupby(["c0", "c1"])
    res = grouped.p.agg(lambda x: all(x > 0))
    # Check that providing a user-defined function in agg()
    # produces the correct index shape when using an object-typed index.
    expected_index = MultiIndex.from_tuples(
        [("x", "x"), ("x", "y")], names=("c0", "c1")
    )
    expected = Series([False, True], index=expected_index, name="p")
    tm.assert_series_equal(res, expected)


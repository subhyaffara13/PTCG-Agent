
def test_as_index_select_column():
    # GH 5764
    df = DataFrame([[1, 2], [1, 4], [5, 6]], columns=["A", "B"])
    result = df.groupby("A", as_index=False)["B"].get_group(1)
    expected = Series([2, 4], name="B")
    tm.assert_series_equal(result, expected)

    result = df.groupby("A", as_index=False, group_keys=True)["B"].apply(
        lambda x: x.cumsum()
    )
    expected = Series([2, 6, 6], name="B", index=range(3))
    tm.assert_series_equal(result, expected)


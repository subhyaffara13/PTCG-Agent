
def test_set_index_update_column():
    df = DataFrame({"a": [1, 2], "b": 1})
    df = df.set_index("a", drop=False)
    expected = df.index.copy(deep=True)
    df.iloc[0, 0] = 100
    tm.assert_index_equal(df.index, expected)


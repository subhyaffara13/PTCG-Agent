
def test_loc_dtype():
    # GH 60600
    df = DataFrame([["a", 1.0, 2.0], ["b", 3.0, 4.0]])
    result = df.loc[0, [1, 2]]
    expected = Series([1.0, 2.0], index=[1, 2], dtype=float, name=0)
    tm.assert_series_equal(result, expected)


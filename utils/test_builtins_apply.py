
def test_builtins_apply(func, value):
    # GH#8155, GH#53974
    # Builtins act as e.g. sum(group), which sums the column labels of group
    df = DataFrame({0: [1, 1, 2], 1: [3, 4, 5], 2: [3, 4, 5]})
    gb = df.groupby(0)
    result = gb.apply(func)

    expected = Series([value, value], index=Index([1, 2], name=0))
    tm.assert_series_equal(result, expected)


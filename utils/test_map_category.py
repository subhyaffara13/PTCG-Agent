
def test_map_category():
    # GH 10324
    a = Series([1, 2, 3, 4])
    b = Series(["even", "odd", "even", "odd"], dtype="category")
    c = Series(["even", "odd", "even", "odd"])

    exp = Series(["odd", "even", "odd", np.nan], dtype="category")
    tm.assert_series_equal(a.map(b), exp)
    exp = Series(["odd", "even", "odd", np.nan])
    tm.assert_series_equal(a.map(c), exp)


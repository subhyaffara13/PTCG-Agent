
def test_transform_absent_categories(all_numeric_accumulations):
    # GH 16771
    # cython transforms with more groups than rows
    x_vals = [1]
    x_cats = range(2)
    y = [1]
    df = DataFrame({"x": Categorical(x_vals, x_cats), "y": y})
    result = getattr(df.y.groupby(df.x, observed=False), all_numeric_accumulations)()
    expected = df.y
    tm.assert_series_equal(result, expected)


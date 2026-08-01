
def test_apply_category_equalness(val):
    # Check if categorical comparisons on apply, GH 21239
    df_values = ["asd", None, 12, "asd", "cde", np.nan]
    df = DataFrame({"a": df_values}, dtype="category")

    result = df.a.apply(lambda x: x == val)
    expected = Series(
        [False if pd.isnull(x) else x == val for x in df_values], name="a"
    )
    # False since behavior of NaN for categorical dtype has been changed (GH 59966)
    tm.assert_series_equal(result, expected)


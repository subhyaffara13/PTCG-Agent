
def test_replace_categorical_series_new_category_raises(to_replace, value):
    # GH 31720
    ser = pd.Series([1, 2, 3], dtype="category")
    with pytest.raises(
        TypeError, match="Cannot setitem on a Categorical with a new category"
    ):
        ser.replace(to_replace, value)


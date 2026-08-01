
def test_astype_categorical():
    arr = period_array(["2000", "2001", "2001", None], freq="D")
    result = arr.astype("category")
    categories = pd.PeriodIndex(["2000", "2001"], freq="D")
    expected = pd.Categorical.from_codes([0, 1, 1, -1], categories=categories)
    tm.assert_categorical_equal(result, expected)


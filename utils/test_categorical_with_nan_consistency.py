
def test_categorical_with_nan_consistency(unit):
    dti = pd.date_range("2012-01-01", periods=5, name="B", unit=unit)
    cat = pd.Categorical.from_codes([-1, 0, 1, 2, 3, 4], categories=dti)
    expected = hash_array(cat, categorize=False)

    ts = pd.Timestamp("2012-01-01").as_unit(unit)
    cat2 = pd.Categorical.from_codes([-1, 0], categories=[ts])
    result = hash_array(cat2, categorize=False)

    assert result[0] in expected
    assert result[1] in expected


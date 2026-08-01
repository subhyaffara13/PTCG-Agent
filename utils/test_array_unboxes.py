
def test_array_unboxes(index_or_series):
    box = index_or_series

    data = box([decimal.Decimal("1"), decimal.Decimal("2")])
    dtype = DecimalDtype2()
    # make sure it works
    with pytest.raises(
        TypeError, match="scalars should not be of type pd.Series or pd.Index"
    ):
        DecimalArray2._from_sequence(data, dtype=dtype)

    result = pd.array(data, dtype="decimal2")
    expected = DecimalArray2._from_sequence(data.values, dtype=dtype)
    tm.assert_equal(result, expected)


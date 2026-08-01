
def test_scalar_setitem_series_with_nested_value(value, indexer_sli):
    # For numeric data, we try to unpack and thus raise for mismatching length
    ser = Series([1, 2, 3])
    with pytest.raises(ValueError, match="setting an array element with a sequence"):
        indexer_sli(ser)[0] = value

    # but for object dtype we preserve the nested data and set as such
    ser = Series([1, "a", "b"], dtype=object)
    indexer_sli(ser)[0] = value
    if isinstance(value, np.ndarray):
        assert (ser.loc[0] == value).all()
    else:
        assert ser.loc[0] == value


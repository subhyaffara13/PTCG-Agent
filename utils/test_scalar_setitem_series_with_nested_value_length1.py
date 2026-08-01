
def test_scalar_setitem_series_with_nested_value_length1(value, indexer_sli):
    # For numeric data, assigning length-1 array to scalar position gets unpacked
    # TODO this only happens in case of ndarray, should we make this consistent
    # for all list-likes? (as happens for DataFrame.(i)loc, see test above)
    ser = Series([1.0, 2.0, 3.0])
    if isinstance(value, np.ndarray):
        indexer_sli(ser)[0] = value
        expected = Series([0.0, 2.0, 3.0])
        tm.assert_series_equal(ser, expected)
    else:
        with pytest.raises(
            ValueError, match="setting an array element with a sequence"
        ):
            indexer_sli(ser)[0] = value

    # but for object dtype we preserve the nested data
    ser = Series([1, "a", "b"], dtype=object)
    indexer_sli(ser)[0] = value
    if isinstance(value, np.ndarray):
        assert (ser.loc[0] == value).all()
    else:
        assert ser.loc[0] == value


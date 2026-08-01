
def test_object_NA_raises_with_skipna_false(all_boolean_reductions):
    # GH#37501
    ser = Series([pd.NA], dtype=object)
    with pytest.raises(TypeError, match="boolean value of NA is ambiguous"):
        ser.groupby([1]).agg(all_boolean_reductions, skipna=False)



def test_getitem_boolean_ea_indexer():
    # GH#45806
    ser = pd.Series([True, False, pd.NA], dtype="boolean")
    result = ser.index[ser]
    expected = Index([0])
    tm.assert_index_equal(result, expected)


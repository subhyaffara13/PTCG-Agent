
def test_drop_non_empty_list(data, index, drop_labels):
    # GH 21494 and GH 16877
    dtype = object if data is None else None
    ser = Series(data=data, index=index, dtype=dtype)
    with pytest.raises(KeyError, match="not found in axis"):
        ser.drop(drop_labels)


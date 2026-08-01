
def test_getitem_fancy(string_series, object_series):
    msg = r"None of \[Index\(\[1, 2, 3\], dtype='int(32|64)'\)\] are in the \[index\]"
    with pytest.raises(KeyError, match=msg):
        string_series[[1, 2, 3]]
    with pytest.raises(KeyError, match=msg):
        object_series[[1, 2, 3]]


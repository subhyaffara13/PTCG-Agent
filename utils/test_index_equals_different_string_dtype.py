
def test_index_equals_different_string_dtype(string_dtype_no_object):
    # GH 61099
    idx_obj = Index(["a", "b", "c"])
    idx_str = Index(["a", "b", "c"], dtype=string_dtype_no_object)

    assert idx_obj.equals(idx_str)
    assert idx_str.equals(idx_obj)


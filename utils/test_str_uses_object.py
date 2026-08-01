
def test_str_uses_object():
    result = SparseDtype(str).subtype
    assert result == np.dtype("object")


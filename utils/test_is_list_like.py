
def test_is_list_like(maybe_list_like):
    obj, expected = maybe_list_like
    expected = True if expected == "set" else expected
    assert inference.is_list_like(obj) == expected


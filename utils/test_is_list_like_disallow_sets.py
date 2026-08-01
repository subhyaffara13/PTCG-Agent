
def test_is_list_like_disallow_sets(maybe_list_like):
    obj, expected = maybe_list_like
    expected = False if expected == "set" else expected
    assert inference.is_list_like(obj, allow_sets=False) == expected


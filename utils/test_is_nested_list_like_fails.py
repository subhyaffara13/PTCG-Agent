
def test_is_nested_list_like_fails(obj):
    assert not inference.is_nested_list_like(obj)


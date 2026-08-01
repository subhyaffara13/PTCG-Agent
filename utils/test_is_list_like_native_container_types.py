
def test_is_list_like_native_container_types():
    # GH 61565
    # is_list_like was yielding false positives for native container types
    assert not inference.is_list_like(list[int])
    assert not inference.is_list_like(list[str])
    assert not inference.is_list_like(tuple[int])
    assert not inference.is_list_like(tuple[str])


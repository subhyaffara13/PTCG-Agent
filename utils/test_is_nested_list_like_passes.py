
def test_is_nested_list_like_passes(inner, outer):
    result = outer([inner for _ in range(5)])
    assert inference.is_list_like(result)


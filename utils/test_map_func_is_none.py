
def test_map_func_is_none():
    with pytest.raises(ValueError, match="The `func` parameter is required"):
        Series([1, 2]).map(func=None)



def test_map_engine_no_function(func):
    s = Series([1, 2])

    with pytest.raises(ValueError, match="engine argument can only be specified"):
        s.map(func, engine="something")


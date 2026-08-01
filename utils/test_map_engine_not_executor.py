
def test_map_engine_not_executor():
    s = Series([1, 2])

    with pytest.raises(ValueError, match="Not a valid engine: 'something'"):
        s.map(lambda x: x, engine="something")


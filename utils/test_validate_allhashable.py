
def test_validate_allhashable():
    assert com.validate_all_hashable(1, "a") is None

    with pytest.raises(TypeError, match="All elements must be hashable"):
        com.validate_all_hashable([])

    with pytest.raises(TypeError, match="list must be a hashable type"):
        com.validate_all_hashable([], error_name="list")



def test_empty_check_in_list() -> None:
    with pytest.raises(TypeError, match="No argument to check!"):
        _api.check_in_list(["a"])


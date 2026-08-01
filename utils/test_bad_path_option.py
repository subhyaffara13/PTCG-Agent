
def test_bad_path_option() -> None:
    with pytest.raises(KeyError):
        oe.contract("a,b,c", [1], [2], [3], optimize="optimall", shapes=True)  # type: ignore


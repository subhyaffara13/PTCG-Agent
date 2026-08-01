
def test_check_in_list_numpy() -> None:
    with pytest.raises(ValueError, match=r"array\(5\) is not a valid value"):
        _api.check_in_list(['a', 'b'], value=np.array(5))



def test_win_type_with_method_invalid():
    pytest.importorskip("scipy")
    with pytest.raises(
        NotImplementedError, match="'single' is the only supported method type."
    ):
        Series(range(1)).rolling(1, win_type="triang", method="table")


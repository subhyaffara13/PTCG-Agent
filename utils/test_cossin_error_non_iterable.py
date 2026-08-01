
def test_cossin_error_non_iterable():
    with pytest.raises(ValueError, match="containing the subblocks of X"):
        cossin(12j)



def test_cossin_error_incorrect_subblocks():
    with pytest.raises(ValueError, match="be due to missing p, q arguments."):
        cossin(([1, 2], [3, 4, 5], [6, 7], [8, 9, 10]))


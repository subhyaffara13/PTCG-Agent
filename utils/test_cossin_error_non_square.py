
def test_cossin_error_non_square():
    with pytest.raises(ValueError, match="only supports square"):
        cossin(np.array([[1, 2]]), 1, 1)



def test_cossin_error_invalid_shape():
    # Invalid x12 dimensions
    p, q = 3, 4
    invalid_x12 = np.ones((p, q + 2))
    valid_ones = np.ones((p, q))
    with pytest.raises(ValueError, 
            match=r"Invalid x12 dimensions: desired \(3, 4\), got \(3, 6\)"):
        cossin((valid_ones, invalid_x12, valid_ones, valid_ones))

    # Invalid x21 dimensions
    invalid_x21 = np.ones(p + 2)
    with pytest.raises(ValueError, 
            match=r"Invalid x21 dimensions: desired \(3, 4\), got \(1, 5\)"):
        cossin((valid_ones, valid_ones, invalid_x21, valid_ones))


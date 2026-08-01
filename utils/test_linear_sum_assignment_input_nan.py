
def test_linear_sum_assignment_input_nan():
    I = np.diag([np.nan, 1, 1])
    with pytest.raises(ValueError, match="contains invalid numeric entries"):
        linear_sum_assignment(I)


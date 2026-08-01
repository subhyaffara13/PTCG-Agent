
def test_linear_sum_assignment_input_neginf():
    I = np.diag([1, -np.inf, 1])
    with pytest.raises(ValueError, match="contains invalid numeric entries"):
        linear_sum_assignment(I)


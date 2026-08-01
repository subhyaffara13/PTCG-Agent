
def test_linear_sum_assignment_input_inf():
    I = np.identity(3)
    I[:, 0] = np.inf
    with pytest.raises(ValueError, match="cost matrix is infeasible"):
        linear_sum_assignment(I)


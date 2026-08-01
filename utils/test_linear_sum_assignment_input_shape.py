
def test_linear_sum_assignment_input_shape():
    with pytest.raises(ValueError, match="expected a matrix"):
        linear_sum_assignment([1, 2, 3])



def test_linear_sum_assignment_input_string():
    I = np.identity(3)
    with pytest.raises(TypeError, match="Cannot cast array data"):
        linear_sum_assignment(I.astype(str))


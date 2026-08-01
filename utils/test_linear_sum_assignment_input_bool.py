
def test_linear_sum_assignment_input_bool():
    I = np.identity(3)
    assert_array_equal(linear_sum_assignment(I.astype(np.bool_)),
                       linear_sum_assignment(I))


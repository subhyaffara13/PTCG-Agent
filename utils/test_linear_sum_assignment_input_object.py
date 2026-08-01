
def test_linear_sum_assignment_input_object():
    C = [[1, 2, 3], [4, 5, 6]]
    assert_array_equal(linear_sum_assignment(C),
                       linear_sum_assignment(np.asarray(C)))
    assert_array_equal(linear_sum_assignment(C),
                       linear_sum_assignment(matrix(C)))


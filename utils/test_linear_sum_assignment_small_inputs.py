
def test_linear_sum_assignment_small_inputs(sign, test_case):
    linear_sum_assignment_assertions(
        linear_sum_assignment, np.array, sign, test_case)


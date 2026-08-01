
def test_min_weight_full_matching_small_inputs(sign, test_case):
    linear_sum_assignment_assertions(
        min_weight_full_bipartite_matching, csr_array, sign, test_case)


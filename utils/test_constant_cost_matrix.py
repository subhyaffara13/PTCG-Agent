
def test_constant_cost_matrix():
    # Fixes #11602
    n = 8
    C = np.ones((n, n))
    row_ind, col_ind = linear_sum_assignment(C)
    assert_array_equal(row_ind, np.arange(n))
    assert_array_equal(col_ind, np.arange(n))



def test_linear_sum_assignment_trivial_cost(num_rows, num_cols):
    C = np.empty(shape=(num_cols, num_rows))
    row_ind, col_ind = linear_sum_assignment(C)
    assert len(row_ind) == 0
    assert len(col_ind) == 0


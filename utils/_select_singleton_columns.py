
def _select_singleton_columns(A, b):
    """
    Finds singleton columns for which the singleton entry is of the same sign
    as the right-hand side; these columns are eligible for inclusion in an
    initial basis. Determines the rows in which the singleton entries are
    located. For each of these rows, returns the indices of the one singleton
    column and its corresponding row.
    """
    # find indices of all singleton columns and corresponding row indices
    column_indices = np.nonzero(np.sum(np.abs(A) != 0, axis=0) == 1)[0]
    columns = A[:, column_indices]          # array of singleton columns
    row_indices = np.zeros(len(column_indices), dtype=int)
    nonzero_rows, nonzero_columns = np.nonzero(columns)
    row_indices[nonzero_columns] = nonzero_rows   # corresponding row indices

    # keep only singletons with entries that have same sign as RHS
    # this is necessary because all elements of BFS must be non-negative
    same_sign = A[row_indices, column_indices]*b[row_indices] >= 0
    column_indices = column_indices[same_sign][::-1]
    row_indices = row_indices[same_sign][::-1]
    # Reversing the order so that steps below select rightmost columns
    # for initial basis, which will tend to be slack variables. (If the
    # guess corresponds with a basic feasible solution but a constraint
    # is not satisfied with the corresponding slack variable zero, the slack
    # variable must be basic.)

    # for each row, keep rightmost singleton column with an entry in that row
    unique_row_indices, first_columns = np.unique(row_indices,
                                                  return_index=True)
    return column_indices[first_columns], unique_row_indices


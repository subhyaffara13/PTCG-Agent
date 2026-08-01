
def _choose_pivot_row(A, B, candidate_rows, pivot_col, Y):
    # Choose row with smallest ratio
    # If there are ties, pick using Bland's rule
    return min(candidate_rows, key=lambda i: (B[i] / A[i, pivot_col], Y[i]))


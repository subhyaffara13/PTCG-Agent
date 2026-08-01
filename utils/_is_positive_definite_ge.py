
def _is_positive_definite_GE(M):
    """A division-free gaussian elimination method for testing
    positive-definiteness."""
    M = M.as_mutable()
    size = M.rows

    for i in range(size):
        is_positive = M[i, i].is_positive
        if is_positive is not True:
            return is_positive
        for j in range(i+1, size):
            M[j, i+1:] = M[i, i] * M[j, i+1:] - M[j, i] * M[i, i+1:]
    return True


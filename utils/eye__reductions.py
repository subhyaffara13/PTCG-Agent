
def eye_Reductions(n):
    return ReductionsOnlyMatrix(n, n, lambda i, j: int(i == j))



def _matrix_mul(M, v):
    return [sum(row[i] * v[i] for i in range(len(v))) for row in M]


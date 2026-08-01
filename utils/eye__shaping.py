
def eye_Shaping(n):
    return ShapingOnlyMatrix(n, n, lambda i, j: int(i == j))



def load_ratio_left(
    M: int, N: int, O: int, P: int, m: int, n: int, o: int, p: int
) -> float:
    """
    compute the ratio of estimated numbers of loads in baseline and b2bgemm
    M, N, O, P are matrix sizes
    m, n, o, p are block sizes
    |       | baseline (lower bound)        | b2bgemm
    | load  | M * N + N * O + M * O + O * P | M / m * P / p * O / o * (o * p + N / n * (m * n + n * o))
    | store | M * O + M * P                 | M * P
    b2bgemm is always better on stores, but for loads we need to find out beneficial cases using this function
    """
    base = M * N + N * O + M * O + O * P
    gemm = (
        ceildiv(M, m)
        * ceildiv(P, p)
        * ceildiv(O, o)
        * (o * p + ceildiv(N, n) * (m * n + n * o))
    )
    return base / gemm


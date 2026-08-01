
def load_ratio_right(
    M: int, N: int, O: int, P: int, m: int, n: int, o: int, p: int
) -> float:
    """
    compute the ratio of estimated numbers of loads in baseline and b2bgemm
    M, N, O, P are matrix sizes
    m, n, o, p are block sizes
    |       | baseline (lower bound)        | b2bgemm
    | load  | N * O + O * P + M * N + N * P | M / m * P / p * N / n * (m * n + O / o * (n * o + o * p))
    | store | N * P + M * P                 | M * P
    b2bgemm is always better on stores, but for loads we need to find out beneficial cases using this function
    """
    base = N * O + O * P + M * N + N * P
    gemm = (
        ceildiv(M, m)
        * ceildiv(P, p)
        * ceildiv(N, n)
        * (m * n + ceildiv(O, o) * (n * o + o * p))
    )
    return base / gemm



def _mood_statistic_no_ties(r, m, n, N, xp):
    rx = r[..., :m]
    M = xp.sum((rx - (N + 1.0) / 2) ** 2, axis=-1)
    E_0_T = m * (N * N - 1.0) / 12
    varM = m * n * (N + 1.0) * (N + 2) * (N - 2) / 180
    return (M - E_0_T) / math.sqrt(varM)


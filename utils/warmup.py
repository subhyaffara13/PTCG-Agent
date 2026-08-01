
def warmup(rg, n=None):
    if n is None:
        n = 11 + np.random.randint(0, 20)
    rg.standard_normal(n)
    rg.standard_normal(n)
    rg.standard_normal(n, dtype=np.float32)
    rg.standard_normal(n, dtype=np.float32)
    rg.integers(0, 2 ** 24, n, dtype=np.uint64)
    rg.integers(0, 2 ** 48, n, dtype=np.uint64)
    rg.standard_gamma(11.0, n)
    rg.standard_gamma(11.0, n, dtype=np.float32)
    rg.random(n, dtype=np.float64)
    rg.random(n, dtype=np.float32)


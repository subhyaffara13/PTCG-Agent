
def _tukey_lmbda_quantile(p, lmbda):
    # For lmbda != 0
    return (p**lmbda - (1 - p)**lmbda)/lmbda


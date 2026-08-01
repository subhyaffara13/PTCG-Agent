
def _numeric_ac(M, mapping):
    # M is a 2D numpy array
    # numeric assortativity coefficient, pearsonr
    import numpy as np

    if M.sum() != 1.0:
        M = M / M.sum()
    x = np.array(list(mapping.keys()))
    y = x  # x and y have the same support
    idx = list(mapping.values())
    a = M.sum(axis=0)
    b = M.sum(axis=1)
    vara = (a[idx] * x**2).sum() - ((a[idx] * x).sum()) ** 2
    varb = (b[idx] * y**2).sum() - ((b[idx] * y).sum()) ** 2
    xy = np.outer(x, y)
    ab = np.outer(a[idx], b[idx])
    return float((xy * (M - ab)).sum() / np.sqrt(vara * varb))


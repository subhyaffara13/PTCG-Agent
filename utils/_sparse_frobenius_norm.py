
def _sparse_frobenius_norm(x):
    data = sp._sputils._todata(x)
    return np.linalg.norm(data)


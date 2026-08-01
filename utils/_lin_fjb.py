
def _lin_fjb(B, x):
    a = np.ones(x.shape[-1], float)
    res = np.concatenate((a, x.ravel()))
    return res.reshape((B.shape[-1], x.shape[-1]))


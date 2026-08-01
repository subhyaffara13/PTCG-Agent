
def _exp_fjb(B, x):
    res = np.concatenate((np.ones(x.shape[-1], float), x * np.exp(B[1] * x)))
    return res.reshape((2, x.shape[-1]))


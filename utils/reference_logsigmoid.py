
def reference_logsigmoid(x):
    return np.where(
        x < 0,
        x - np.log1p(np.exp(x)),
        -np.log1p(np.exp(-x)))



def reference_sigmoid(x):
    # 'scipy.special.expit' not supported for the input types
    if x.dtype in [np.complex64, np.complex128]:
        return (1 / (1 + np.exp(-x)))
    return scipy.special.expit(x)


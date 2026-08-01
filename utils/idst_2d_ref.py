
def idst_2d_ref(x, **kwargs):
    """Calculate reference values for testing idst2."""
    x = np.array(x, copy=True)
    for row in range(x.shape[0]):
        x[row, :] = idst(x[row, :], **kwargs)
    for col in range(x.shape[1]):
        x[:, col] = idst(x[:, col], **kwargs)
    return x


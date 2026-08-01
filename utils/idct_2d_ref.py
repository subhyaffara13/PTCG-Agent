
def idct_2d_ref(x, **kwargs):
    """Calculate reference values for testing idct2."""
    x = np.array(x, copy=True)
    for row in range(x.shape[0]):
        x[row, :] = idct(x[row, :], **kwargs)
    for col in range(x.shape[1]):
        x[:, col] = idct(x[:, col], **kwargs)
    return x


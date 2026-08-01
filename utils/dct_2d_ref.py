
def dct_2d_ref(x, **kwargs):
    """Calculate reference values for testing dct2."""
    x = np.array(x, copy=True)
    for row in range(x.shape[0]):
        x[row, :] = dct(x[row, :], **kwargs)
    for col in range(x.shape[1]):
        x[:, col] = dct(x[:, col], **kwargs)
    return x



def dst_2d_ref(x, **kwargs):
    """Calculate reference values for testing dst2."""
    x = np.array(x, copy=True)
    for row in range(x.shape[0]):
        x[row, :] = dst(x[row, :], **kwargs)
    for col in range(x.shape[1]):
        x[:, col] = dst(x[:, col], **kwargs)
    return x


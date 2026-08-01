
def _squeeze_ref(x, axis=None):
    # NumPy doesn't allow squeezing scalars
    if x.ndim == 0:
        return x

    if isinstance(axis, Sequence):
        # Numpy doesn't allow specifying non-singular dimensions
        axis = tuple(a for a in axis if x.shape[a] == 1)

    if isinstance(axis, int) and x.shape[axis] != 1:
        return x

    return np.squeeze(x, axis)


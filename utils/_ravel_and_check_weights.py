
def _ravel_and_check_weights(a, weights):
    """ Check a and weights have matching shapes, and ravel both """
    a = np.asarray(a)

    # Ensure that the array is a "subtractable" dtype
    if a.dtype == np.bool:
        msg = f"Converting input from {a.dtype} to {np.uint8} for compatibility."
        warnings.warn(msg, RuntimeWarning, stacklevel=3)
        a = a.astype(np.uint8)

    if weights is not None:
        weights = np.asarray(weights)
        if weights.shape != a.shape:
            raise ValueError(
                'weights should have the same shape as a.')
        weights = weights.ravel()
    a = a.ravel()
    return a, weights


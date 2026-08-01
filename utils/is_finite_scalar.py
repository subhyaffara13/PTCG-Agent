
def is_finite_scalar(x):
    """Test whether `x` is either a finite scalar or a finite array scalar.

    """
    return np.size(x) == 1 and np.isfinite(x)


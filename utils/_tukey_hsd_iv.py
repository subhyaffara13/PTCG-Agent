
def _tukey_hsd_iv(args, equal_var):
    if (len(args)) < 2:
        raise ValueError("There must be more than 1 treatment.")
    if not isinstance(equal_var, bool):
        raise TypeError("Expected a boolean value for 'equal_var'")
    args = [np.asarray(arg) for arg in args]
    for arg in args:
        if arg.ndim != 1:
            raise ValueError("Input samples must be one-dimensional.")
        if arg.size <= 1:
            raise ValueError("Input sample size must be greater than one.")
        if np.isinf(arg).any():
            raise ValueError("Input samples must be finite.")
    return args


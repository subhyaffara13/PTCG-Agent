
def _arr_to_scalar(x):
    # If x is a numpy array, return x.item().  This will
    # fail if the array has more than one element.
    return x.item() if isinstance(x, np.ndarray) else x


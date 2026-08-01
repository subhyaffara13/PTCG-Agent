
def _find_nonzero_rows(A, tol):
    """
    Returns logical array indicating the locations of rows with at least
    one nonzero element.
    """
    return np.any(np.abs(A) > tol, axis=1)



def _format_b_constraints(b):
    """Format the upper bounds of the constraints to a 1-D array

    Parameters
    ----------
    b : 1-D array
        1-D array of values representing the upper-bound of each (in)equality
        constraint (row) in ``A``.

    Returns
    -------
    1-D np.array
        1-D array of values representing the upper-bound of each (in)equality
        constraint (row) in ``A``.

    """
    if b is None:
        return np.array([], dtype=float)
    b = np.array(b, dtype=float, copy=True).squeeze()
    return b if b.size != 1 else b.reshape(-1)


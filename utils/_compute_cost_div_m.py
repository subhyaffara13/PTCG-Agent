
def _compute_cost_div_m(m, p, norm_info):
    """
    A helper function for computing bounds.

    This is equation (3.10).
    It measures cost in terms of the number of required matrix products.

    Parameters
    ----------
    m : int
        A valid key of _theta.
    p : int
        A matrix power.
    norm_info : LazyOperatorNormInfo
        Information about 1-norms of related operators.

    Returns
    -------
    cost_div_m : int
        Required number of matrix products divided by m.

    """
    return int(np.ceil(norm_info.alpha(p) / _theta[m]))


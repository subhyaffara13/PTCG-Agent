
def _validate_marginal_input(dimensions, multivariate_dims):
    """Determine if input dimensions can be marginalized.

    Parameters
    ----------
    dimensions : float, ndarray
        Input dimensions to be marginalized
    multivariate_dims : int
        Number of dimensions of multivariate distribution.

    Returns
    -------
    dims : ndarray
        Array of indices to marginalize
    """
    dims = np.copy(dimensions)
    dims = np.atleast_1d(dims)

    if len(dims) == 0:
        msg = "Cannot marginalize all dimensions."
        raise ValueError(msg)

    if not np.issubdtype(dims.dtype, np.integer):
        msg = ("Elements of `dimensions` must be integers - the indices "
               "of the marginal variables being retained.")
        raise ValueError(msg)

    original_dims = np.copy(dims)

    dims[dims < 0] += multivariate_dims

    if len(np.unique(dims)) != len(dims):
        msg = "All elements of `dimensions` must be unique."
        raise ValueError(msg)

    i_invalid = (dims < 0) | (dims >= multivariate_dims)
    if np.any(i_invalid):
        msg = (f"Dimensions {original_dims[i_invalid]} are invalid "
               f"for a distribution in {multivariate_dims} dimensions.")
        raise ValueError(msg)

    return dims


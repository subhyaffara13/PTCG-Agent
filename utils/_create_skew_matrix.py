
def _create_skew_matrix(vec: Array) -> Array:
    """Create skew-symmetric (aka cross-product) matrix for stack of vectors."""
    xp = array_namespace(vec)
    result = xp.zeros((*vec.shape[:-1], 3, 3), dtype=vec.dtype, device=xp_device(vec))
    result = xpx.at(result)[..., 0, 1].set(-vec[..., 2])
    result = xpx.at(result)[..., 0, 2].set(vec[..., 1])
    result = xpx.at(result)[..., 1, 0].set(vec[..., 2])
    result = xpx.at(result)[..., 1, 2].set(-vec[..., 0])
    result = xpx.at(result)[..., 2, 0].set(-vec[..., 1])
    result = xpx.at(result)[..., 2, 1].set(vec[..., 0])
    return result


def _create_skew_matrix(x):
    """Create skew-symmetric matrices corresponding to vectors.

    Parameters
    ----------
    x : ndarray, shape (n, 3)
        Set of vectors.

    Returns
    -------
    ndarray, shape (n, 3, 3)
    """
    result = np.zeros((len(x), 3, 3))
    result[:, 0, 1] = -x[:, 2]
    result[:, 0, 2] = x[:, 1]
    result[:, 1, 0] = x[:, 2]
    result[:, 1, 2] = -x[:, 0]
    result[:, 2, 0] = -x[:, 1]
    result[:, 2, 1] = x[:, 0]
    return result


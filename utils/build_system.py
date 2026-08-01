
def build_system(interpolation):
    """
    Build the left-hand side matrix of the interpolation system. The
    matrix below stores W * diag(right_scaling),
    where W is the theoretical matrix of the interpolation system. The
    right scaling matrices is chosen to keep the elements in
    the matrix well-balanced.

    Parameters
    ----------
    interpolation : `cobyqa.models.Interpolation`
        Interpolation set.
    """

    _cache = interpolation._lhs_cache
    # Compute the scaled directions from the base point to the
    # interpolation points. We scale the directions to avoid numerical
    # difficulties.
    if _cache is not None and np.array_equal(
        interpolation.xpt, _cache["xpt"]
    ):
        return _cache["a"], _cache["right_scaling"], _cache["eigh"]

    scale = np.max(np.linalg.norm(interpolation.xpt, axis=0), initial=EPS)
    xpt_scale = interpolation.xpt / scale

    n, npt = xpt_scale.shape
    a = np.zeros((npt + n + 1, npt + n + 1))
    a[:npt, :npt] = 0.5 * (xpt_scale.T @ xpt_scale) ** 2.0
    a[:npt, npt] = 1.0
    a[:npt, npt + 1:] = xpt_scale.T
    a[npt, :npt] = 1.0
    a[npt + 1:, :npt] = xpt_scale

    # Build the left and right scaling diagonal matrices.
    right_scaling = np.empty(npt + n + 1)
    right_scaling[:npt] = 1.0 / scale**2.0
    right_scaling[npt] = scale**2.0
    right_scaling[npt + 1:] = scale

    eig_values, eig_vectors = eigh(a, check_finite=False)

    new_cache = {
        "xpt": np.copy(interpolation.xpt),
        "a": np.copy(a),
        "right_scaling": np.copy(right_scaling),
        "eigh": (eig_values, eig_vectors),
    }
    interpolation._lhs_cache = new_cache

    return a, right_scaling, (eig_values, eig_vectors)


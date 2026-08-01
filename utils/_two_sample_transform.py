
def _two_sample_transform(u, v):
    """Helper function that concatenates x and y for two sample MGC stat.

    See above for use.

    Parameters
    ----------
    u, v : ndarray
        `u` and `v` have shapes ``(n, p)`` and ``(m, p)``.

    Returns
    -------
    x : ndarray
        Concatenate `u` and `v` along the ``axis = 0``. `x` thus has shape
        ``(2n, p)``.
    y : ndarray
        Label matrix for `x` where 0 refers to samples that comes from `u` and
        1 refers to samples that come from `v`. `y` thus has shape ``(2n, 1)``.

    """
    nx = u.shape[0]
    ny = v.shape[0]
    x = np.concatenate([u, v], axis=0)
    y = np.concatenate([np.zeros(nx), np.ones(ny)], axis=0).reshape(-1, 1)
    return x, y



def _mgc_stat(distx, disty):
    r"""Helper function that calculates the MGC stat. See above for use.

    Parameters
    ----------
    distx, disty : ndarray
        `distx` and `disty` have shapes ``(n, p)`` and ``(n, q)`` or
        ``(n, n)`` and ``(n, n)``
        if distance matrices.

    Returns
    -------
    stat : float
        The sample MGC test statistic within ``[-1, 1]``.
    stat_dict : dict
        Contains additional useful additional returns containing the following
        keys:

        - stat_mgc_map : ndarray
            MGC-map of the statistics.
        - opt_scale : (float, float)
            The estimated optimal scale as a ``(x, y)`` pair.

    """
    # calculate MGC map and optimal scale
    stat_mgc_map = _local_correlations(distx, disty, global_corr='mgc')

    m, n = stat_mgc_map.shape
    if m == 1 or n == 1:
        # the global scale at is the statistic calculated at maximal nearest
        # neighbors. There is not enough local scale to search over, so
        # default to global scale
        stat = stat_mgc_map[m - 1][n - 1]
        opt_scale = m * n
    else:
        samp_size = len(distx) - 1

        # threshold to find connected region of significant local correlations
        sig_connect = _threshold_mgc_map(stat_mgc_map, samp_size)

        # maximum within the significant region
        stat, opt_scale = _smooth_mgc_map(sig_connect, stat_mgc_map)

    stat_dict = {"stat_mgc_map": stat_mgc_map,
                 "opt_scale": opt_scale}

    return stat, stat_dict


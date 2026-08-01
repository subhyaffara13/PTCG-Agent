
def _smooth_mgc_map(sig_connect, stat_mgc_map):
    """Finds the smoothed maximal within the significant region R.

    If area of R is too small it returns the last local correlation. Otherwise,
    returns the maximum within significant_connected_region.

    Parameters
    ----------
    sig_connect : ndarray
        A binary matrix with 1's indicating the significant region.
    stat_mgc_map : ndarray
        All local correlations within ``[-1, 1]``.

    Returns
    -------
    stat : float
        The sample MGC statistic within ``[-1, 1]``.
    opt_scale: (float, float)
        The estimated optimal scale as an ``(x, y)`` pair.

    """
    m, n = stat_mgc_map.shape

    # the global scale at is the statistic calculated at maximal nearest
    # neighbors. By default, statistic and optimal scale are global.
    stat = stat_mgc_map[m - 1][n - 1]
    opt_scale = [m, n]

    if np.linalg.norm(sig_connect) != 0:
        # proceed only when the connected region's area is sufficiently large
        # 0.02 is simply an empirical threshold, this can be set to 0.01 or 0.05
        # with varying levels of performance
        if np.sum(sig_connect) >= np.ceil(0.02 * max(m, n)) * min(m, n):
            max_corr = max(stat_mgc_map[sig_connect])

            # find all scales within significant_connected_region that maximize
            # the local correlation
            max_corr_index = np.where((stat_mgc_map >= max_corr) & sig_connect)

            if max_corr >= stat:
                stat = max_corr

                k, l = max_corr_index
                one_d_indices = k * n + l  # 2D to 1D indexing
                k = np.max(one_d_indices) // n
                l = np.max(one_d_indices) % n
                opt_scale = [k+1, l+1]  # adding 1s to match R indexing

    return stat, opt_scale



def _threshold_mgc_map(stat_mgc_map, samp_size):
    r"""
    Finds a connected region of significance in the MGC-map by thresholding.

    Parameters
    ----------
    stat_mgc_map : ndarray
        All local correlations within ``[-1,1]``.
    samp_size : int
        The sample size of original data.

    Returns
    -------
    sig_connect : ndarray
        A binary matrix with 1's indicating the significant region.

    """
    m, n = stat_mgc_map.shape

    # 0.02 is simply an empirical threshold, this can be set to 0.01 or 0.05
    # with varying levels of performance. Threshold is based on a beta
    # approximation.
    per_sig = 1 - (0.02 / samp_size)  # Percentile to consider as significant
    threshold = samp_size * (samp_size - 3)/4 - 1/2  # Beta approximation
    threshold = distributions.beta.ppf(per_sig, threshold, threshold) * 2 - 1

    # the global scale at is the statistic calculated at maximal nearest
    # neighbors. Threshold is the maximum on the global and local scales
    threshold = max(threshold, stat_mgc_map[m - 1][n - 1])

    # find the largest connected component of significant correlations
    sig_connect = stat_mgc_map > threshold
    if np.sum(sig_connect) > 0:
        sig_connect, _ = _measurements.label(sig_connect)
        _, label_counts = np.unique(sig_connect, return_counts=True)

        # skip the first element in label_counts, as it is count(zeros)
        max_label = np.argmax(label_counts[1:]) + 1
        sig_connect = sig_connect == max_label
    else:
        sig_connect = np.array([[False]])

    return sig_connect


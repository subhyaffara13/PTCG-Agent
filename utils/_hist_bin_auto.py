
def _hist_bin_auto(x, range):
    """
    Histogram bin estimator that uses the minimum width of a relaxed
    Freedman-Diaconis and Sturges estimators if the FD bin width does
    not result in a large number of bins. The relaxed Freedman-Diaconis estimator
    limits the bin width to half the sqrt estimated to avoid small bins.

    The FD estimator is usually the most robust method, but its width
    estimate tends to be too large for small `x` and bad for data with limited
    variance. The Sturges estimator is quite good for small (<1000) datasets
    and is the default in the R language. This method gives good off-the-shelf
    behaviour.


    Parameters
    ----------
    x : array_like
        Input data that is to be histogrammed, trimmed to range. May not
        be empty.
    range : Tuple with range for the histogram

    Returns
    -------
    h : An estimate of the optimal bin width for the given data.

    See Also
    --------
    _hist_bin_fd, _hist_bin_sturges
    """
    fd_bw = _hist_bin_fd(x, range)
    sturges_bw = _hist_bin_sturges(x, range)
    sqrt_bw = _hist_bin_sqrt(x, range)
    # heuristic to limit the maximal number of bins
    fd_bw_corrected = max(fd_bw, sqrt_bw / 2)
    return min(fd_bw_corrected, sturges_bw)


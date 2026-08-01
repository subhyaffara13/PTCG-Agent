
def find_peaks_cwt(vector, widths, wavelet=None, max_distances=None,
                   gap_thresh=None, min_length=None,
                   min_snr=1, noise_perc=10, window_size=None):
    """
    Find peaks in a 1-D array with wavelet transformation.

    The general approach is to smooth `vector` by convolving it with
    `wavelet(width)` for each width in `widths`. Relative maxima which
    appear at enough length scales, and with sufficiently high SNR, are
    accepted.

    Parameters
    ----------
    vector : ndarray
        1-D array in which to find the peaks.
    widths : float or sequence
        Single width or 1-D array-like of widths to use for calculating
        the CWT matrix. In general,
        this range should cover the expected width of peaks of interest.
    wavelet : callable, optional
        Should take two parameters and return a 1-D array to convolve
        with `vector`. The first parameter determines the number of points
        of the returned wavelet array, the second parameter is the scale
        (`width`) of the wavelet. Should be normalized and symmetric.
        Default is the ricker wavelet.
    max_distances : ndarray, optional
        At each row, a ridge line is only connected if the relative max at
        ``row[n]`` is within ``max_distances[n]`` from the relative max at
        ``row[n+1]``.  Default value is ``widths/4``.
    gap_thresh : float, optional
        If a relative maximum is not found within `max_distances`,
        there will be a gap. A ridge line is discontinued if there are more
        than `gap_thresh` points without connecting a new relative maximum.
        Default is the first value of the widths array i.e. ``widths[0]``.
    min_length : int, optional
        Minimum length a ridge line needs to be acceptable.
        Default is ``cwt.shape[0] / 4``, ie 1/4-th the number of widths.
    min_snr : float, optional
        Minimum SNR ratio. Default 1. The signal is the maximum CWT coefficient
        on the largest ridge line. The noise is `noise_perc` th percentile of
        datapoints contained within the same ridge line.
    noise_perc : float, optional
        When calculating the noise floor, percentile of data points
        examined below which to consider noise. Calculated using
        `stats.scoreatpercentile`.  Default is 10.
    window_size : int, optional
        Size of window to use to calculate noise floor.
        Default is ``cwt.shape[1] / 20``.

    Returns
    -------
    peaks_indices : ndarray
        Indices of the locations in the `vector` where peaks were found.
        The list is sorted.

    See Also
    --------
    find_peaks
        Find peaks inside a signal based on peak properties.

    Notes
    -----
    This approach was designed for finding sharp peaks among noisy data,
    however with proper parameter selection it should function well for
    different peak shapes.

    The algorithm is as follows:
     1. Perform a continuous wavelet transform on `vector`, for the supplied
        `widths`. This is a convolution of `vector` with `wavelet(width)` for
        each width in `widths`.
     2. Identify "ridge lines" in the cwt matrix. These are relative maxima
        at each row, connected across adjacent rows. See identify_ridge_lines
     3. Filter the ridge_lines using filter_ridge_lines.

    References
    ----------
    .. [1] Bioinformatics (2006) 22 (17): 2059-2065.
       :doi:`10.1093/bioinformatics/btl355`

    Examples
    --------
    >>> import numpy as np
    >>> from scipy import signal
    >>> xs = np.arange(0, np.pi, 0.05)
    >>> data = np.sin(xs)
    >>> peakind = signal.find_peaks_cwt(data, np.arange(1,10))
    >>> peakind, xs[peakind], data[peakind]
    ([32], array([ 1.6]), array([ 0.9995736]))

    """
    widths = np.atleast_1d(np.asarray(widths))

    if gap_thresh is None:
        gap_thresh = np.ceil(widths[0])
    if max_distances is None:
        max_distances = widths / 4.0
    if wavelet is None:
        wavelet = _ricker

    cwt_dat = _cwt(vector, wavelet, widths)
    ridge_lines = _identify_ridge_lines(cwt_dat, max_distances, gap_thresh)
    filtered = _filter_ridge_lines(cwt_dat, ridge_lines, min_length=min_length,
                                   window_size=window_size, min_snr=min_snr,
                                   noise_perc=noise_perc)
    max_locs = np.asarray([x[1][0] for x in filtered])
    max_locs.sort()

    return max_locs



def _select_by_peak_threshold(x, peaks, tmin, tmax):
    """
    Evaluate which peaks fulfill the threshold condition.

    Parameters
    ----------
    x : ndarray
        A 1-D array which is indexable by `peaks`.
    peaks : ndarray
        Indices of peaks in `x`.
    tmin, tmax : scalar or ndarray or None
         Minimal and / or maximal required thresholds. If supplied as ndarrays
         their size must match `peaks`. ``None`` is interpreted as an open
         border.

    Returns
    -------
    keep : bool
        A boolean mask evaluating to true where `peaks` fulfill the threshold
        condition.
    left_thresholds, right_thresholds : ndarray
        Array matching `peak` containing the thresholds of each peak on
        both sides.

    Notes
    -----

    .. versionadded:: 1.1.0
    """
    # Stack thresholds on both sides to make min / max operations easier:
    # tmin is compared with the smaller, and tmax with the greater threshold to
    # each peak's side
    stacked_thresholds = np.vstack([x[peaks] - x[peaks - 1],
                                    x[peaks] - x[peaks + 1]])
    keep = np.ones(peaks.size, dtype=bool)
    if tmin is not None:
        min_thresholds = np.min(stacked_thresholds, axis=0)
        keep &= (tmin <= min_thresholds)
    if tmax is not None:
        max_thresholds = np.max(stacked_thresholds, axis=0)
        keep &= (max_thresholds <= tmax)

    return keep, stacked_thresholds[0], stacked_thresholds[1]


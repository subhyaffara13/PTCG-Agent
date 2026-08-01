
def whittaker_henderson(signal, *, lamb="reml", order=2, weights=None):
    r"""
    Whittaker-Henderson (WH) smoothing/graduation of a discrete signal.

    This implements WH smoothing with a difference penalty of the specified ``order``
    and penalty strength ``lamb``, see [1]_, [2]_ and [3]_. WH can be seen as a
    penalized B-Spline (P-Spline) of degree zero for equidistant knots at the signal
    positions.

    In econometrics, the WH graduation of order 2 is referred to as the
    Hodrick-Prescott filter [4]_.
    
    Parameters
    ----------
    signal : array_like
        A one-dimensional array of length ``order + 1`` representing equidistant data
        points of a signal, e.g. a time series with constant time lag.
    
    lamb : str or float, optional
        Smoothing or penalty parameter, default is ``"reml"`` which minimizes the
        restricted maximum likelihood (REML) criterion to find the parameter ``lamb``.
        If a number is passed, it must be non-negative and it is used directly.

    order : int, default: 2
        The order of the difference penalty, must be at least 1.

    weights : array_like or None, optional
        A one-dimensional array of case weights with the same length as `signal`.
        ``None`` is equivalent to an array of all ones, ``np.ones_like(signal)``.

    Returns
    -------
     res : _RichResult
        An object similar to an instance of `scipy.optimize.OptimizeResult` with the
        following attributes:

        x : ndarray
            The WH smoothed signal.
        lamb : float
            The penalty parameter. If the input ``lamb`` is a number, this value is
            returned. If the input was ``"reml"``, the penalty parameter that minimized
            the REML criterion is returned.

    Notes
    -----
    For the signal :math:`y = (y_1, y_2, \ldots, y_n)` and weights
    :math:`w = (w_1, w_2, \ldots, w_n)`, WH of order :math:`p` with smoothing or
    penalty parameter :math:`\lambda` solves the following optimization problem for
    :math:`x_i`:

    .. math::

        \operatorname{argmin}_{x_i} \sum_i^n w_i (y_i - x_i)^2
        + \lambda \sum_i^{n-p} (\Delta^p x_i)^2 \,,

    where :math:`\Delta^p` is the forward difference operator of order :math:`p`,
    :math:`\Delta x_i = x_{i+1} - x_i` and
    :math:`\Delta^2 x_i = \Delta(\Delta x_i) = x_{i+2} - 2x_{i+1} + x_i`.
    For every input value :math:`y_i`, it generates a smoothed value :math:`x_i`.

    One of the nice properties of WH is that it automatically performs inter- and
    extrapolation of data. Interpolation means filling in values when signal data is
    only available on the left and on the right. Extrapolation means filling in values
    after the observed signal ends.
    Set ``weights = 0`` for regions where you want to extra- or interpolate. The values
    of `signal` don't matter if ``weights = 0``.
    WH interpolates a polynomial of ``degree = 2 * order - 1`` and it extrapolates a
    polynomial of ``degree = order - 1``. For ``order = 2``, this means cubic
    interpolation and linear extrapolation.

    References
    ----------
    .. [1] Whittaker-Henderson smoothing,
           https://en.wikipedia.org/wiki/Whittaker%E2%80%93Henderson_smoothing
    .. [2] Eilers, P.H.C. (2003).
           "A perfect smoother". Analytical Chem. 75, 3631-3636.
           :doi:`10.1021/AC034173T`
    .. [3] Weinert, Howard L. (2007).
           "Efficient computation for Whittaker-Henderson smoothing".
           Computational Statistics and Data Analysis 52:959-74.
           :doi:`10.1016/j.csda.2006.11.038`
    .. [4] Hodrick, R. J., and Prescott, E. C. (1997).
           "Postwar U.S. Business Cycles: An Empirical Investigation".
           :doi:`10.2307/2953682`

    Examples
    --------
    We use data from https://data.giss.nasa.gov/gistemp/ for global temperature
    anomalies, i.e., deviations from the corresponding 1951-1980 means (Combined
    Land-Surface Air and Sea-Surface Water Temperature Anomalies, Land-Ocean Temperature
    Index, L-OTI).
    We use weights to indicate where to inter- and extrapolate the missing data.

    >>> from pathlib import Path
    >>> import numpy as np
    >>> import scipy
    >>> from scipy.signal import whittaker_henderson
    >>> # For the most recent data, use
    ... # fname="https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
    ... # Here, we instead use a copy made in 2026.
    ... fname = Path(scipy.signal.__file__).parent / "tests/data/GLB.Ts+dSST.csv"
    >>> data = np.genfromtxt(
    ...     fname=fname,
    ...     delimiter=",", skip_header=2, missing_values="***"
    ... )
    >>> year = data[:, 0]
    >>> temperature = data[:, 1:13].ravel()  # monthly temperature anomalies
    >>> w = np.ones_like(temperature)
    >>> # We might have some nan values.
    ... np.sum(np.isnan(temperature))
    np.int64(10)
    >>> w[np.isnan(temperature)] = 0
    >>> res = whittaker_henderson(temperature, weights=w)
    >>> temperature[:5]
    array([-0.19, -0.25, -0.09, -0.16, -0.1])
    >>> res.x[:5]
    array([-0.18244619, -0.17823282, -0.17409373, -0.17080896, -0.16833158])

    Let us plot measurements and Whittaker-Henderson smoothing.

    >>> import matplotlib.pyplot as plt
    >>> x = year[0] + np.arange(len(temperature)) / 12
    >>> plt.plot(x, temperature, label="measurement")
    >>> plt.plot(x, res.x, label="WH smooth")
    >>> # Above, we set w = 0 for nan values of temperature. WH automatically
    ... # inter- or extrapolates for all data points with w = 0.
    ... plt.plot(x[w==0], res.x[w==0], color="red", label="inter-/extrapolation")
    >>> plt.xlabel("year")
    >>> plt.ylabel("temperature deviation [°C]")
    >>> plt.title("Global Temperature Anomalies (ref. 1951-1980)")
    >>> plt.legend()
    >>> plt.show()

    We can see that extrapolation has occurred at the right end of the signal, meaning
    that NaNs existed in the data for the most recent dates, in particular months of
    2026 that have not yet happened at the time of the data download in March 2026.

    """
    order = _validate_int(order, name="order", minimum=1)

    signal = np.asarray(signal)
    if signal.ndim != 1:
        msg = f"Input array signal must be of shape (n,); got {signal.shape}"
        raise ValueError(msg)

    n = signal.shape[0]
    if n < order + 1:
        msg = f"Input array signal must be at least of shape ({order + 1},); got {n}."
        raise ValueError(msg)

    if weights is not None:
        weights = np.asarray(weights)
        if weights.shape != signal.shape:
            msg = "Input array weights must have the same shape as the signal array."
            raise ValueError(msg)
        
    if weights is None:
        if not np.isfinite(signal).all():
            raise ValueError("Input array signal must be finite.")
    else:
        if not np.isfinite(weights).all():
            raise ValueError("Input array weights must be finite.")
        if (mask := ~np.isfinite(signal)).any():
            # Only weights * y matter in the end and weights must be 0 for all
            # non-finite elements of signal.
            if not (weights[mask] == 0).all():
                raise ValueError("Input array weights must be zero for all non-finite "
                                 "elements of signal.")
            signal = np.nan_to_num(signal)


    msg = f"Parameter lamb must be string 'reml' or a non-negative float; got {lamb=}."
    if isinstance(lamb, str):
        if lamb != "reml":
            raise ValueError(msg)
        def criterion(loglamb):
            return -_reml(lamb=np.exp(loglamb), y=signal, order=order, weights=weights)
        opt = minimize_scalar(criterion, bracket=[-10, 10])
        lamb = np.exp(opt.x)

    if lamb < 0:
        raise ValueError(msg)
    elif lamb == 0.0:
        x = np.asarray(signal).copy()
    else:
        x, _ = _solve_WH_banded(signal, lamb=lamb, order=order, weights=weights)
    return _RichResult(x=x, lamb=lamb)


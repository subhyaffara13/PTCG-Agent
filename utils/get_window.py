
def get_window(window, Nx, fftbins=True, *, xp=None, device=None):
    r"""Convenience function for creating various windows.

    This function is a wrapper for the window functions provided in the
    `scipy.signal.windows` namespace.

    Parameters
    ----------
    window : str | tuple | float
        Either a string with the window name or a tuple consisting of window name and
        window parameters. If it is a float, a `~scipy.singal.kaiser` window is
        created with `window` being the shape parameter. Consult the Notes below for
        more details.
    Nx : int
        The number of samples in the window.
    fftbins : bool, optional
        If ``True`` (default), create a periodic window, ready to use with `ifftshift`
        and be multiplied by the result of an FFT (see also
        :func:`~scipy.fft.fftfreq`). If ``False``, create a symmetric window, for use
        in filter design. This parameter is ignored, if the window name in the
        `window` parameter has a suffix ``'_periodic'`` or ``'_symmetric'`` appended to
        it (e.g., ``'hann_symmetric'``).
    %(xp_device_snippet)s

    Returns
    -------
    get_window : ndarray
        Returns the created window as a one-dimensional array made of `Nx` samples.

    Raises
    ------
    ValueError
        If the provided parameters do not allow to choose a valid window function
        with valid parameters.

    Notes
    -----
    Note that by default this function returns a periodic window, whereas the wrapped
    window functions return a symmetric window by default. This is caused by the
    `fftbins` parameter having the inverse meaning of the `sym` parameter of the
    wrapped function, which are both ``True`` by default.

    .. currentmodule:: scipy.signal.windows

    The following list shows the wrapped window functions with the respective settings
    of the `window` parameter followed by a short description. Aliases for alternative
    window names are given in parenthesis.

    `barthann` / ``'barthann'``:
        Modified Bartlett-Hann window (aliases: ``'brthan', 'bth'``)
    `bartlett` / ``'bartlett'``:
        Bartlett window (aliases: ``'bart', 'brt'``)
    `blackman`/ ``'blackman'``:
        Blackman window (aliases: ``'black', 'blk'``)
    `blackmanharris` / ``'blackmanharris'``:
        4-term Blackman-Harris window (aliases: ``'blackharr', 'bkh'``)
    `bohman` / ``'bohman'``:
        Bohman window (aliases: ``'bman', 'bmn'``)
    `boxcar` / ``'boxcar'``:
        Rectangular window (aliases: ``'box', 'ones', 'rect', 'rectangular'``)
    `chebwin` / ``('chebwin', at)``:
        Dolph-Chebyshev window with `at` dB attenuation (aliases: ``'cheb'``)
    `cosine` / ``'cosine'``:
        Cosine window (aliases: ``'halfcosine'``)
    `dpss` / ``('dpss', NW)``:
        First window of discrete prolate spheroidal sequence with standardized half
        bandwidth ``NW`` and "approximate" norm.
    `exponential` / ``'exponential'`` / ``('exponential', center, tau)``:
        Exponential / Poisson window centered at ``center`` (default: ``None``) with
        deacy ``tau`` (default: ``1``) (aliases: ``'poisson'``)
    `flattop`/ ``'flattop'``:
        Flat top window (aliases: ``'flat', 'flt'``)
    `gaussian` / ``('gaussian', std)``:
        Gaussian with standard deviation `std` (aliases: ``'gauss', 'gss'``)
    `general_cosine` / ``('general cosine', a)``:
        Generic weighted sum of cosine terms with weighting coefficients ``a``
        (aliases: ``'general_cosine'``)
    `general_gaussian` / ``('general gaussian', p, sig)``:
        Generalized Gaussian with shape parameter ``p`` and standard deviation ``sig``
        (aliases: ``'general_gaussian', 'general gauss', 'general_gauss', 'ggs'``)
    `general_hamming` / ``('general hamming', alpha)``:
        Generalized Hamming window with coefficent ``alpha``
        (aliases: ``'general_hamming'``)
    `hamming` / ``'hamming'``:
        Hamming window (aliases: ``'hamm', 'ham'``)
    `hann` / ``'hann'``:
        Hann window (aliases: ``'han'``)
    `kaiser` / ``('kaiser', beta)``:
        Kaiser window with shape parameter ``beta`` (aliases: ``'ksr'``)
    `kaiser_bessel_derived` / ``('kaiser bessel derived', beta)``:
        Kaiser-Bessel derived window with shape parameter ``beta``
        (aliases: ``'kaiser_bessel_derived', 'kbd'``)
    `lanczos` / ``'lanczos'``:
        Lanczos / sinc window (aliases: ``'sinc'``)
    `nuttall`/ ``'nuttall'``:
        Minimum 4-term Blackman-Harris window according to Nuttall
        (aliases: ``'nutl', 'nut'``)
    `parzen` / ``'parzen'``:
        Parzen window (aliases: ``'parz', 'par'``)
    `taylor` / ``'taylor'`` / (``'taylor', nbar, sll, norm)``:
        Taylor window with ``nbar`` adjascent sidelobes (default: ``4``)), ``sll`` dB
        suppression level (default: ``30``) and boolean value ``norm``
        (default: ``True``) (aliases: ``taylorwin``)
    `triang`/ ``'triangle'``:
        Triangle window (aliases: ``'triang', 'tri'``)
    `tukey` / ``'tukey'`` / ``('tukey', alpha)``:
        Tukey window with shape parameter ``alpha`` (default: ``0.5``)
        (aliases: ``'tuk'``)


    Examples
    --------
    This example shows different usages of the `window` parameter:

    >>> from scipy.signal import get_window
    >>> get_window('triang', 7)
    array([ 0.125,  0.375,  0.625,  0.875,  0.875,  0.625,  0.375])
    >>> get_window(('exponential', None, 1.), 9)
    array([ 0.011109  ,  0.03019738,  0.082085  ,  0.22313016,  0.60653066,
            0.60653066,  0.22313016,  0.082085  ,  0.03019738])
    >>> get_window(('kaiser', 4.0), 9)
    array([ 0.08848053,  0.29425961,  0.56437221,  0.82160913,  0.97885093,
            0.97885093,  0.82160913,  0.56437221,  0.29425961])
    >>> get_window(4.0, 9)  # same as previous call
    array([ 0.08848053,  0.29425961,  0.56437221,  0.82160913,  0.97885093,
            0.97885093,  0.82160913,  0.56437221,  0.29425961])

    The following snippet shows different ways to create identical symmetric and
    periodic Bartlett windows:

    >>> from scipy.signal import get_window, windows
    >>> # Symmetric window:
    >>> windows.bartlett(5)  # Parameter `sym` defaults to True
    array([0. , 0.5, 1. , 0.5, 0. ])
    >>> get_window('bartlett', 5, fftbins=False)
    array([0. , 0.5, 1. , 0.5, 0. ])
    >>> get_window('bartlett_symmetric', 5)
    array([0. , 0.5, 1. , 0.5, 0. ])
    >>> # Periodic window:
    >>> windows.bartlett(4, sym=False)
    array([0. , 0.5, 1. , 0.5])
    >>> get_window('bartlett', 4)  # Parameter `fftbins` defaults to True
    array([0. , 0.5, 1. , 0.5])
    >>> get_window('bartlett_periodic', 4)
    array([0. , 0.5, 1. , 0.5])
    >>> # `_periodic' suffix overrides `fftbins` parameter:
    >>> get_window('bartlett_periodic', 4, fftbins=False)
    array([0. , 0.5, 1. , 0.5])

    Note that a periodic window can be created out of a symmetric window by discarding
    the last sample.
    """
    if not (Nx > 0 and isinstance(Nx, numbers.Integral)):
        raise ValueError(f"Parameter {Nx=} is not a positive integer")
    if not isinstance(fftbins, bool):
        raise ValueError(f"Parameter {fftbins=} is not of type bool!")

    if not isinstance(window, str | tuple):
        try: # if parameter window can be converted to a float, return kaiser window:
            beta = float(window)
        except Exception as float_exception:
            err_msg = f"Parameter {window=} must be a tuple, a string or a float!"
            raise ValueError(err_msg) from float_exception
        return kaiser(Nx, beta, not fftbins, xp=xp, device=device)

    if isinstance(window, tuple) and not isinstance(window[0], str):
        raise ValueError(f"First tuple entry of parameter {window=} is not a str!")

    sym = not fftbins
    win_name = window if isinstance(window, str) else window[0]
    if win_name.endswith('_symmetric'):  # overwrite `fftbins` / `sym` if needed
        sym, win_name = True, win_name[:-10]  # remove '_symmetric' from `win_name`
    elif win_name.endswith('_periodic'):
        sym, win_name = False, win_name[:-9]  # remove '_periodic' from `win_name`

    if win_name not in _WIN_FUNCS:
        raise ValueError(f"Invalid window name '{win_name}' in parameter {window=}!")

    func, has_args = _WIN_FUNCS[win_name]
    args = window[1:] if isinstance(window, tuple) else tuple()
    if len(args) > 0 and has_args is False:
        raise ValueError(f"'{win_name}' does not allow parameters, but {window=}!")
    if len(args) == 0 and has_args is True:
        raise ValueError(f"'{win_name}' must have parameters, but {window=}!")
    # has_args == 'OPTIONAL' allows len(args) == 0 as well as len(args) > 0

    if not has_args:
        return func(Nx, sym=sym, xp=xp, device=device)

    # special cases taken from original implementation:
    if func is dpss:
        if len(args) != 1:
            raise ValueError(f"Window {win_name} must have one parameter but {window=}")
        return dpss(Nx, args[0], Kmax=None, sym=sym, xp=xp, device=device)
    if func is general_cosine:
        if not (xp is None and device is None):
            raise ValueError("'general_cosine' does not accept the parameters xp " +
                             "and device not being None!")
        return general_cosine(Nx, *args, sym=sym)

    return func(Nx, *args, sym=sym, xp=xp, device=device)


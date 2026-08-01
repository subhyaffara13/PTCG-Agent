
def group_delay(system, w=512, whole=False, fs=2*pi):
    r"""Compute the group delay of a digital filter.

    The group delay measures by how many samples amplitude envelopes of
    various spectral components of a signal are delayed by a filter.
    It is formally defined as the derivative of continuous (unwrapped) phase::

               d        jw
     D(w) = - -- arg H(e)
              dw

    Parameters
    ----------
    system : tuple of array_like (b, a)
        Numerator and denominator coefficients of a filter transfer function.
    w : {None, int, array_like}, optional
        If a single integer, then compute at that many frequencies (default is
        N=512).

        If an array_like, compute the delay at the frequencies given. These
        are in the same units as `fs`.
    whole : bool, optional
        Normally, frequencies are computed from 0 to the Nyquist frequency,
        fs/2 (upper-half of unit-circle). If `whole` is True, compute
        frequencies from 0 to fs. Ignored if w is array_like.
    fs : float, optional
        The sampling frequency of the digital system. Defaults to 2*pi
        radians/sample (so w is from 0 to pi).

        .. versionadded:: 1.2.0

    Returns
    -------
    w : ndarray
        The frequencies at which group delay was computed, in the same units
        as `fs`.  By default, `w` is normalized to the range [0, pi)
        (radians/sample).
    gd : ndarray
        The group delay.

    See Also
    --------
    freqz : Frequency response of a digital filter

    Notes
    -----
    The similar function in MATLAB is called `grpdelay`.

    If the transfer function :math:`H(z)` has zeros or poles on the unit
    circle, the group delay at corresponding frequencies is undefined.
    When such a case arises the warning is raised and the group delay
    is set to 0 at those frequencies.

    For the details of numerical computation of the group delay refer to [1]_ or [2]_.

    .. versionadded:: 0.16.0

    References
    ----------
    .. [1] Richard G. Lyons, "Understanding Digital Signal Processing,
           3rd edition", p. 830.
    .. [2] Julius O. Smith III, "Numerical Computation of Group Delay",
           in "Introduction to Digital Filters with Audio Applications",
           online book, 2007,
           https://ccrma.stanford.edu/~jos/fp/Numerical_Computation_Group_Delay.html

    Examples
    --------
    >>> from scipy import signal
    >>> b, a = signal.iirdesign(0.1, 0.3, 5, 50, ftype='cheby1')
    >>> w, gd = signal.group_delay((b, a))

    >>> import matplotlib.pyplot as plt
    >>> plt.title('Digital filter group delay')
    >>> plt.plot(w, gd)
    >>> plt.ylabel('Group delay [samples]')
    >>> plt.xlabel('Frequency [rad/sample]')
    >>> plt.show()

    """
    xp = array_namespace(*system, w)
    b, a = map(np.atleast_1d, system)

    if w is None:
        # For backwards compatibility
        w = 512

    fs = _validate_fs(fs, allow_none=False)

    if _is_int_type(w):
        if whole:
            w = np.linspace(0, 2 * pi, w, endpoint=False)
        else:
            w = np.linspace(0, pi, w, endpoint=False)
    else:
        w = np.atleast_1d(w)
        w = 2*pi*w/fs

    c = np.convolve(b, np.conjugate(a[::-1]))
    cr = c * np.arange(c.size)
    z = np.exp(-1j * w)
    num = np.polyval(cr[::-1], z)
    den = np.polyval(c[::-1], z)
    gd = np.real(num / den) - a.size + 1
    singular = ~np.isfinite(gd)
    near_singular = np.absolute(den) < 10 * EPSILON

    if np.any(singular):
        gd[singular] = 0
        warnings.warn(
            "The group delay is singular at frequencies "
            f"[{', '.join(f'{ws:.3f}' for ws in w[singular])}], setting to 0",
            stacklevel=2
        )

    elif np.any(near_singular):
        warnings.warn(
            "The filter's denominator is extremely small at frequencies "
            f"[{', '.join(f'{ws:.3f}' for ws in w[near_singular])}], "
            "around which a singularity may be present",
            stacklevel=2
        )

    w = w * (fs / (2 * xp.pi))

    return xp.asarray(w), xp.asarray(gd)


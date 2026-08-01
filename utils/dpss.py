
def dpss(M, NW, Kmax=None, sym=True, norm=None, return_ratios=False,
         *, xp=None, device=None):
    """
    Compute the Discrete Prolate Spheroidal Sequences (DPSS).

    DPSS (or Slepian sequences) are often used in multitaper power spectral
    density estimation (see [1]_). The first window in the sequence can be
    used to maximize the energy concentration in the main lobe, and is also
    called the Slepian window.

    Parameters
    ----------
    M : int
        Window length.
    NW : float
        Standardized half bandwidth corresponding to ``2*NW = BW/f0 = BW*M*dt``
        where ``dt`` is taken as 1.
    Kmax : int | None, optional
        Number of DPSS windows to return (orders ``0`` through ``Kmax-1``).
        If None (default), return only a single window of shape ``(M,)``
        instead of an array of windows of shape ``(Kmax, M)``.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    norm : {2, 'approximate', 'subsample'} | None, optional
        If 'approximate' or 'subsample', then the windows are normalized by the
        maximum, and a correction scale-factor for even-length windows
        is applied either using ``M**2/(M**2+NW)`` ("approximate") or
        a FFT-based subsample shift ("subsample"), see Notes for details.
        If None, then "approximate" is used when ``Kmax=None`` and 2 otherwise
        (which uses the l2 norm).
    return_ratios : bool, optional
        If True, also return the concentration ratios in addition to the
        windows.
    %(xp_device_snippet)s

    Returns
    -------
    v : ndarray, shape (Kmax, M) or (M,)
        The DPSS windows. Will be 1D if `Kmax` is None.
    r : ndarray, shape (Kmax,) or float, optional
        The concentration ratios for the windows. Only returned if
        `return_ratios` evaluates to True. Will be 0D if `Kmax` is None.

    Notes
    -----
    This computation uses the tridiagonal eigenvector formulation given
    in [2]_.

    The default normalization for ``Kmax=None``, i.e. window-generation mode,
    simply using the l-infinity norm would create a window with two unity
    values, which creates slight normalization differences between even and odd
    orders. The approximate correction of ``M**2/float(M**2+NW)`` for even
    sample numbers is used to counteract this effect (see Examples below).

    For very long signals (e.g., 1e6 elements), it can be useful to compute
    windows orders of magnitude shorter and use interpolation (e.g.,
    `scipy.interpolate.interp1d`) to obtain tapers of length `M`,
    but this in general will not preserve orthogonality between the tapers.

    .. versionadded:: 1.1

    References
    ----------
    .. [1] Percival DB, Walden WT. Spectral Analysis for Physical Applications:
       Multitaper and Conventional Univariate Techniques.
       Cambridge University Press; 1993.
    .. [2] Slepian, D. Prolate spheroidal wave functions, Fourier analysis, and
       uncertainty V: The discrete case. Bell System Technical Journal,
       Volume 57 (1978), 1371430.
    .. [3] Kaiser, JF, Schafer RW. On the Use of the I0-Sinh Window for
       Spectrum Analysis. IEEE Transactions on Acoustics, Speech and
       Signal Processing. ASSP-28 (1): 105-107; 1980.

    Examples
    --------
    We can compare the window to `kaiser`, which was invented as an alternative
    that was easier to calculate [3]_ (example adapted from
    `here <https://ccrma.stanford.edu/~jos/sasp/Kaiser_DPSS_Windows_Compared.html>`_):

    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> from scipy.signal import windows, freqz
    >>> M = 51
    >>> fig, axes = plt.subplots(3, 2, figsize=(5, 7))
    >>> for ai, alpha in enumerate((1, 3, 5)):
    ...     win_dpss = windows.dpss(M, alpha)
    ...     beta = alpha*np.pi
    ...     win_kaiser = windows.kaiser(M, beta)
    ...     for win, c in ((win_dpss, 'k'), (win_kaiser, 'r')):
    ...         win /= win.sum()
    ...         axes[ai, 0].plot(win, color=c, lw=1.)
    ...         axes[ai, 0].set(xlim=[0, M-1], title=rf'$\\alpha$ = {alpha}',
    ...                         ylabel='Amplitude')
    ...         w, h = freqz(win)
    ...         axes[ai, 1].plot(w, 20 * np.log10(np.abs(h)), color=c, lw=1.)
    ...         axes[ai, 1].set(xlim=[0, np.pi],
    ...                         title=rf'$\\beta$ = {beta:0.2f}',
    ...                         ylabel='Magnitude (dB)')
    >>> for ax in axes.ravel():
    ...     ax.grid(True)
    >>> axes[2, 1].legend(['DPSS', 'Kaiser'])
    >>> fig.tight_layout()
    >>> plt.show()

    And here are examples of the first four windows, along with their
    concentration ratios:

    >>> M = 512
    >>> NW = 2.5
    >>> win, eigvals = windows.dpss(M, NW, 4, return_ratios=True)
    >>> fig, ax = plt.subplots(1)
    >>> ax.plot(win.T, linewidth=1.)
    >>> ax.set(xlim=[0, M-1], ylim=[-0.1, 0.1], xlabel='Samples',
    ...        title=f'DPSS, {M:d}, {NW:0.1f}')
    >>> ax.legend([f'win[{ii}] ({ratio:0.4f})'
    ...            for ii, ratio in enumerate(eigvals)])
    >>> fig.tight_layout()
    >>> plt.show()

    Using a standard :math:`l_{\\infty}` norm would produce two unity values
    for even `M`, but only one unity value for odd `M`. This produces uneven
    window power that can be counteracted by the approximate correction
    ``M**2/float(M**2+NW)``, which can be selected by using
    ``norm='approximate'`` (which is the same as ``norm=None`` when
    ``Kmax=None``, as is the case here). Alternatively, the slower
    ``norm='subsample'`` can be used, which uses subsample shifting in the
    frequency domain (FFT) to compute the correction:

    >>> Ms = np.arange(1, 41)
    >>> factors = (50, 20, 10, 5, 2.0001)
    >>> energy = np.empty((3, len(Ms), len(factors)))
    >>> for mi, M in enumerate(Ms):
    ...     for fi, factor in enumerate(factors):
    ...         NW = M / float(factor)
    ...         # Corrected using empirical approximation (default)
    ...         win = windows.dpss(M, NW)
    ...         energy[0, mi, fi] = np.sum(win ** 2) / np.sqrt(M)
    ...         # Corrected using subsample shifting
    ...         win = windows.dpss(M, NW, norm='subsample')
    ...         energy[1, mi, fi] = np.sum(win ** 2) / np.sqrt(M)
    ...         # Uncorrected (using l-infinity norm)
    ...         win /= win.max()
    ...         energy[2, mi, fi] = np.sum(win ** 2) / np.sqrt(M)
    >>> fig, ax = plt.subplots(1)
    >>> hs = ax.plot(Ms, energy[2], '-o', markersize=4,
    ...              markeredgecolor='none')
    >>> leg = [hs[-1]]
    >>> for hi, hh in enumerate(hs):
    ...     h1 = ax.plot(Ms, energy[0, :, hi], '-o', markersize=4,
    ...                  color=hh.get_color(), markeredgecolor='none',
    ...                  alpha=0.66)
    ...     h2 = ax.plot(Ms, energy[1, :, hi], '-o', markersize=4,
    ...                  color=hh.get_color(), markeredgecolor='none',
    ...                  alpha=0.33)
    ...     if hi == len(hs) - 1:
    ...         leg.insert(0, h1[0])
    ...         leg.insert(0, h2[0])
    >>> ax.set(xlabel='M (samples)', ylabel=r'Power / $\\sqrt{M}$')
    >>> ax.legend(leg, ['Uncorrected', r'Corrected: $\\frac{M^2}{M^2+NW}$',
    ...                 'Corrected (subsample)'])
    >>> fig.tight_layout()

    """
    xp = _namespace(xp)

    if norm is None:
        norm = 'approximate' if Kmax is None else 2
    known_norms = (2, 'approximate', 'subsample')
    if norm not in known_norms:
        raise ValueError(f'norm must be one of {known_norms}, got {norm}')
    if Kmax is None:
        singleton = True
        Kmax = 1
    else:
        singleton = False
    if _len_guards(M):
        if not return_ratios:
            return xp.ones(M, dtype=xp.float64)
        elif singleton:
            return xp.ones(M, dtype=xp.float64), 1.
        else:
            return xp.ones(M, dtype=xp.float64), xp.ones(1, dtype=xp.float64)
    Kmax = operator.index(Kmax)
    if not 0 < Kmax <= M:
        raise ValueError('Kmax must be greater than 0 and less than M')
    if NW >= M/2.:
        raise ValueError('NW must be less than M/2.')
    if NW <= 0:
        raise ValueError('NW must be positive')
    M, needs_trunc = _extend(M, sym)
    W = float(NW) / M
    nidx = xp.arange(M, dtype=xp.float64, device=device)

    # Here we want to set up an optimization problem to find a sequence
    # whose energy is maximally concentrated within band [-W,W].
    # Thus, the measure lambda(T,W) is the ratio between the energy within
    # that band, and the total energy. This leads to the eigen-system
    # (A - (l1)I)v = 0, where the eigenvector corresponding to the largest
    # eigenvalue is the sequence with maximally concentrated energy. The
    # collection of eigenvectors of this system are called Slepian
    # sequences, or discrete prolate spheroidal sequences (DPSS). Only the
    # first K, K = 2NW/dt orders of DPSS will exhibit good spectral
    # concentration
    # [see https://en.wikipedia.org/wiki/Spectral_concentration_problem]

    # Here we set up an alternative symmetric tri-diagonal eigenvalue
    # problem such that
    # (B - (l2)I)v = 0, and v are our DPSS (but eigenvalues l2 != l1)
    # the main diagonal = ([M-1-2*t]/2)**2 cos(2PIW), t=[0,1,2,...,M-1]
    # and the first off-diagonal = t(M-t)/2, t=[1,2,...,M-1]
    # [see Percival and Walden, 1993]
    d = ((M - 1 - 2 * nidx) / 2.) ** 2 * xp.cos(xp.asarray(2 * xp.pi * W))
    e = nidx[1:] * (M - nidx[1:]) / 2.

    # only calculate the highest Kmax eigenvalues
    w, windows = linalg.eigh_tridiagonal(
        d, e, select='i', select_range=(M - Kmax, M - 1))
    w = w[::-1]
    windows = windows[:, ::-1].T

    # By convention (Percival and Walden, 1993 pg 379)
    # * symmetric tapers (k=0,2,4,...) should have a positive average.
    fix_even = (windows[::2, ...].sum(axis=1) < 0)
    for i, f in enumerate(fix_even):
        if f:
            windows[2 * i] *= -1
    # * antisymmetric tapers should begin with a positive lobe
    #   (this depends on the definition of "lobe", here we'll take the first
    #   point above the numerical noise, which should be good enough for
    #   sufficiently smooth functions, and more robust than relying on an
    #   algorithm that uses max(abs(w)), which is susceptible to numerical
    #   noise problems)
    thresh = max(1e-7, 1. / M)
    for i, w in enumerate(windows[1::2, ...]):
        if w[w * w > thresh][0] < 0:
            windows[2 * i + 1] *= -1

    # Now find the eigenvalues of the original spectral concentration problem
    # Use the autocorr sequence technique from Percival and Walden, 1993 pg 390
    if return_ratios:
        dpss_rxx = _fftautocorr(xp.asarray(windows))
        r = 4 * W * xpx.sinc(xp.asarray(2 * W * nidx), xp=xp)
        r[0] = 2 * W
        ratios = xp.matmul(dpss_rxx, r)
        if singleton:
            ratios = ratios[0]
        ratios = xp.asarray(ratios, device=device)
    # Deal with sym and Kmax=None
    if norm != 2:
        windows /= windows.max()
        if M % 2 == 0:
            if norm == 'approximate':
                correction = M**2 / float(M**2 + NW)
            else:
                s = sp_fft.rfft(windows[0])
                shift = -(1 - 1./M) * xp.arange(1, M//2 + 1, dtype=xp.float64)
                s[1:] *= 2 * xp.exp(-1j * xp.pi * shift)
                correction = M / s.real.sum()
            windows *= correction
    # else we're already l2 normed, so do nothing
    if needs_trunc:
        windows = windows[:, :-1]
    if singleton:
        windows = windows[0]
    windows = xp.asarray(windows, device=device)
    return (windows, ratios) if return_ratios else windows


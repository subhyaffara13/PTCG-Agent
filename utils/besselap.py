import math


def besselap(N, norm='phase', *, xp=None, device=None):
    """
    Return (z,p,k) for analog prototype of an Nth-order Bessel filter.

    Parameters
    ----------
    N : int
        The order of the filter.
    norm : {'phase', 'delay', 'mag'}, optional
        Frequency normalization:

        ``phase``
            The filter is normalized such that the phase response reaches its
            midpoint at an angular (e.g., rad/s) cutoff frequency of 1. This
            happens for both low-pass and high-pass filters, so this is the
            "phase-matched" case. [6]_

            The magnitude response asymptotes are the same as a Butterworth
            filter of the same order with a cutoff of `Wn`.

            This is the default, and matches MATLAB's implementation.

        ``delay``
            The filter is normalized such that the group delay in the passband
            is 1 (e.g., 1 second). This is the "natural" type obtained by
            solving Bessel polynomials

        ``mag``
            The filter is normalized such that the gain magnitude is -3 dB at
            angular frequency 1. This is called "frequency normalization" by
            Bond. [1]_

        .. versionadded:: 0.18.0

    %(xp_device_snippet)s

    Returns
    -------
    z : ndarray[float64]
        Zeros of the transfer function. Is always an empty array.
    p : ndarray[complex128]
        Poles of the transfer function.
    k : float
        Gain of the transfer function. For phase-normalized, this is always 1.

    See Also
    --------
    bessel : Filter design function using this prototype

    Notes
    -----
    To find the pole locations, approximate starting points are generated [2]_
    for the zeros of the ordinary Bessel polynomial [3]_, then the
    Aberth-Ehrlich method [4]_ [5]_ is used on the Kv(x) Bessel function to
    calculate more accurate zeros, and these locations are then inverted about
    the unit circle.

    References
    ----------
    .. [1] C.R. Bond, "Bessel Filter Constants",
           http://www.crbond.com/papers/bsf.pdf
    .. [2] Campos and Calderon, "Approximate closed-form formulas for the
           zeros of the Bessel Polynomials", :arXiv:`1105.0957`.
    .. [3] Thomson, W.E., "Delay Networks having Maximally Flat Frequency
           Characteristics", Proceedings of the Institution of Electrical
           Engineers, Part III, November 1949, Vol. 96, No. 44, pp. 487-490.
    .. [4] Aberth, "Iteration Methods for Finding all Zeros of a Polynomial
           Simultaneously", Mathematics of Computation, Vol. 27, No. 122,
           April 1973
    .. [5] Ehrlich, "A modified Newton method for polynomials", Communications
           of the ACM, Vol. 10, Issue 2, pp. 107-108, Feb. 1967,
           :doi:`10.1145/363067.363115`.
    .. [6] Miller and Bohn, "A Bessel Filter Crossover, and Its Relation to
           Others", RaneNote 147, 1998,
           https://www.ranecommercial.com/legacy/note147.html

    """
    if xp is None:
        xp = np_compat

    if abs(int(N)) != N:
        raise ValueError("Filter order must be a nonnegative integer")

    N = int(N)  # calculation below doesn't always fit in np.int64
    if N == 0:
        p = []
        k = 1
    else:
        # Find roots of reverse Bessel polynomial
        p = 1/_bessel_zeros(N)

        a_last = _falling_factorial(2*N, N) // 2**N

        # Shift them to a different normalization if required
        if norm in ('delay', 'mag'):
            # Normalized for group delay of 1
            k = a_last
            if norm == 'mag':
                # -3 dB magnitude point is at 1 rad/sec
                norm_factor = _norm_factor(p, k)
                p /= norm_factor
                k = norm_factor**-N * a_last
        elif norm == 'phase':
            # Phase-matched (1/2 max phase shift at 1 rad/sec)
            # Asymptotes are same as Butterworth filter
            p *= 10**(-math.log10(a_last)/N)
            k = 1
        else:
            raise ValueError('normalization not understood')

    z = xp.asarray([], device=device, dtype=xp.float64)
    return (
        z,
        xp.asarray(p, device=device, dtype=xp.complex128),
        float(k)
    )


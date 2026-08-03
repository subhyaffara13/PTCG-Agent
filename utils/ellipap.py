import math


def ellipap(N, rp, rs, *, xp=None, device=None):
    """Return (z,p,k) of Nth-order elliptic analog lowpass filter.

    The filter is a normalized prototype that has `rp` decibels of ripple
    in the passband and a stopband `rs` decibels down.

    The filter's angular (e.g., rad/s) cutoff frequency is normalized to 1,
    defined as the point at which the gain first drops below ``-rp``.

    Parameters
    ----------
    N : int
        The order of the filter
    rp : float
        The passband ripple intensity
    rs : float
        The stopband attenuation
    %(xp_device_snippet)s

    Returns
    -------
    z : ndarray[complex128]
        Zeros of the transfer function.
    p : ndarray[complex128]
        Poles of the transfer function.
    k : float
        Gain of the transfer function.

    See Also
    --------
    ellip : Filter design function using this prototype

    References
    ----------
    .. [1] Lutovac, Tosic, and Evans, "Filter Design for Signal Processing",
           Chapters 5 and 12.

    .. [2] Orfanidis, "Lecture Notes on Elliptic Filter Design",
           https://www.ece.rutgers.edu/~orfanidi/ece521/notes.pdf

    """
    if xp is None:
        xp = np_compat

    if abs(int(N)) != N:
        raise ValueError("Filter order must be a nonnegative integer")
    elif N == 0:
        # Avoid divide-by-zero warning
        # Even order filters have DC gain of -rp dB
        return (
            xp.asarray([], device=device, dtype=xp.complex128),
            xp.asarray([], device=device, dtype=xp.complex128),
            10**(-rp/20)
        )
    elif N == 1:
        p = -math.sqrt(1.0 / _pow10m1(0.1 * rp))
        k = -p
        z = []
        return (
            xp.asarray(z, device=device, dtype=xp.complex128),
            xp.asarray(p, device=device, dtype=xp.complex128), k
        )

    eps_sq = _pow10m1(0.1 * rp)

    eps = math.sqrt(eps_sq)
    ck1_sq = eps_sq / _pow10m1(0.1 * rs)
    if ck1_sq == 0:
        raise ValueError("Cannot design a filter with given rp and rs"
                         " specifications.")

    # do computations with numpy, xp.asarray the return values

    val = special.ellipk(ck1_sq), special.ellipkm1(ck1_sq)

    m = _ellipdeg(N, ck1_sq)

    capk = special.ellipk(m)

    j = np.arange(1 - N % 2, N, 2)
    jj = len(j)

    [s, c, d, phi] = special.ellipj(j * capk / N, m * np.ones(jj))
    snew = np.compress(abs(s) > EPSILON, s, axis=-1)
    z = 1.0 / (np.sqrt(m) * snew)
    z = 1j * z
    z = np.concatenate((z, np.conjugate(z)))

    r = _arc_jac_sc1(1. / eps, ck1_sq)
    v0 = capk * r / (N * val[0])

    [sv, cv, dv, phi] = special.ellipj(v0, 1 - m)
    p = -(c * d * sv * cv + 1j * s * dv) / (1 - (d * sv) ** 2.0)

    if N % 2:
        newp = np.compress(
            abs(p.imag) > EPSILON * np.sqrt(np.sum(p * np.conjugate(p), axis=0).real),
            p, axis=-1
        )
        p = np.concatenate((p, np.conjugate(newp)))
    else:
        p = np.concatenate((p, np.conjugate(p)))

    k = (np.prod(-p, axis=0) / np.prod(-z, axis=0)).real
    if N % 2 == 0:
        k = k / np.sqrt(1 + eps_sq)

    return (
        xp.asarray(z, device=device, dtype=xp.complex128),
        xp.asarray(p, device=device, dtype=xp.complex128), float(k)
    )


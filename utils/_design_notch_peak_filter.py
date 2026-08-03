import math


def _design_notch_peak_filter(w0, Q, ftype, fs=2.0, *, xp=None, device=None):
    """
    Design notch or peak digital filter.

    Parameters
    ----------
    w0 : float
        Normalized frequency to remove from a signal. If `fs` is specified,
        this is in the same units as `fs`. By default, it is a normalized
        scalar that must satisfy  ``0 < w0 < 1``, with ``w0 = 1``
        corresponding to half of the sampling frequency.
    Q : float
        Quality factor. Dimensionless parameter that characterizes
        notch filter -3 dB bandwidth ``bw`` relative to its center
        frequency, ``Q = w0/bw``.
    ftype : str
        The type of IIR filter to design:

            - notch filter : ``notch``
            - peak filter  : ``peak``
    fs : float, optional
        The sampling frequency of the digital system.

        .. versionadded:: 1.2.0:

    Returns
    -------
    b, a : ndarray, ndarray
        Numerator (``b``) and denominator (``a``) polynomials
        of the IIR filter.
    """
    if xp is None:
        xp = np_compat

    fs = _validate_fs(fs, allow_none=False)

    # Guarantee that the inputs are floats
    w0 = float(w0)
    Q = float(Q)
    w0 = 2 * w0 / fs

    # Checks if w0 is within the range
    if w0 > 1.0 or w0 < 0.0:
        raise ValueError("w0 should be such that 0 < w0 < 1")

    # Get bandwidth
    bw = w0/Q

    # Normalize inputs
    bw = bw * xp.pi
    w0 = w0 * xp.pi

    if ftype not in ("notch", "peak"):
        raise ValueError("Unknown ftype.")

    # Compute beta according to Eqs. 11.3.4 (p.575) and 11.3.19 (p.579) from
    # reference [1]. Due to assuming a -3 dB attenuation value, i.e, assuming
    # gb = 1 / np.sqrt(2), the following terms simplify to:
    #   (np.sqrt(1.0 - gb**2.0) / gb) = 1
    #   (gb / np.sqrt(1.0 - gb**2.0)) = 1
    beta = math.tan(bw / 2.0)

    # Compute gain: formula 11.3.6 (p.575) from reference [1]
    gain = 1.0 / (1.0 + beta)

    # Compute numerator b and denominator a
    # formulas 11.3.7 (p.575) and 11.3.21 (p.579)
    # from reference [1]
    if ftype == "notch":
        b = gain * xp.asarray([1.0, -2.0*math.cos(w0), 1.0], device=device)
    else:
        b = (1.0 - gain) * xp.asarray([1.0, 0.0, -1.0], device=device)
    a = xp.asarray([1.0, -2.0 * gain * math.cos(w0), (2.0*gain - 1.0)], device=device)

    return b, a


import math


def cheb2ord(wp, ws, gpass, gstop, analog=False, fs=None):
    """Chebyshev type II filter order selection.

    Return the order of the lowest order digital or analog Chebyshev Type II
    filter that loses no more than `gpass` dB in the passband and has at least
    `gstop` dB attenuation in the stopband.

    Parameters
    ----------
    wp, ws : float
        Passband and stopband edge frequencies.

        For digital filters, these are in the same units as `fs`. By default,
        `fs` is 2 half-cycles/sample, so these are normalized from 0 to 1,
        where 1 is the Nyquist frequency. (`wp` and `ws` are thus in
        half-cycles / sample.)  For example:

        - Lowpass:   wp = 0.2,          ws = 0.3
        - Highpass:  wp = 0.3,          ws = 0.2
        - Bandpass:  wp = [0.2, 0.5],   ws = [0.1, 0.6]
        - Bandstop:  wp = [0.1, 0.6],   ws = [0.2, 0.5]

        For analog filters, `wp` and `ws` are angular frequencies (e.g., rad/s).
    gpass : float
        The maximum loss in the passband (dB).
    gstop : float
        The minimum attenuation in the stopband (dB).
    analog : bool, optional
        When True, return an analog filter, otherwise a digital filter is
        returned.
    fs : float, optional
        The sampling frequency of the digital system.

        .. versionadded:: 1.2.0

    Returns
    -------
    ord : int
        The lowest order for a Chebyshev type II filter that meets specs.
    wn : ndarray or float
        The Chebyshev natural frequency (the "3dB frequency") for use with
        `cheby2` to give filter results. If `fs` is specified,
        this is in the same units, and `fs` must also be passed to `cheby2`.

    See Also
    --------
    cheby2 : Filter design using order and critical points
    buttord : Find order and critical points from passband and stopband spec
    cheb1ord, ellipord
    iirfilter : General filter design using order and critical frequencies
    iirdesign : General filter design using passband and stopband spec

    Examples
    --------
    Design a digital bandstop filter which rejects -60 dB from 0.2*(fs/2) to
    0.5*(fs/2), while staying within 3 dB below 0.1*(fs/2) or above
    0.6*(fs/2). Plot its frequency response, showing the passband and
    stopband constraints in gray.

    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np

    >>> N, Wn = signal.cheb2ord([0.1, 0.6], [0.2, 0.5], 3, 60)
    >>> b, a = signal.cheby2(N, 60, Wn, 'stop')
    >>> w, h = signal.freqz(b, a)
    >>> plt.semilogx(w / np.pi, 20 * np.log10(abs(h)))
    >>> plt.title('Chebyshev II bandstop filter fit to constraints')
    >>> plt.xlabel('Normalized frequency')
    >>> plt.ylabel('Amplitude [dB]')
    >>> plt.grid(which='both', axis='both')
    >>> plt.fill([.01, .1, .1, .01], [-3,  -3, -99, -99], '0.9', lw=0) # stop
    >>> plt.fill([.2,  .2, .5,  .5], [ 9, -60, -60,   9], '0.9', lw=0) # pass
    >>> plt.fill([.6,  .6,  2,   2], [-99, -3,  -3, -99], '0.9', lw=0) # stop
    >>> plt.axis([0.06, 1, -80, 3])
    >>> plt.show()

    """
    xp = array_namespace(wp, ws)
    wp, ws = map(xp.asarray, (wp, ws))

    fs = _validate_fs(fs, allow_none=True)
    _validate_gpass_gstop(gpass, gstop)
    wp, ws, filter_type = _validate_wp_ws(wp, ws, fs, analog, xp=xp)
    passb, stopb = _pre_warp(wp, ws, analog, xp=xp)
    nat, passb = _find_nat_freq(stopb, passb, gpass, gstop, filter_type, 'cheby', xp=xp)

    GSTOP = 10 ** (0.1 * builtins.abs(gstop))
    GPASS = 10 ** (0.1 * builtins.abs(gpass))
    v_pass_stop = math.acosh(math.sqrt((GSTOP - 1.0) / (GPASS - 1.0)))
    ord = int(xp.ceil(v_pass_stop / xp.acosh(nat)))

    # Find frequency where analog response is -gpass dB.
    # Then convert back from low-pass prototype to the original filter.

    new_freq = math.cosh(1.0 / ord * v_pass_stop)
    new_freq = 1.0 / new_freq

    if filter_type == 1:
        nat = passb / new_freq
    elif filter_type == 2:
        nat = passb * new_freq
    elif filter_type == 3:
        nat0 = (new_freq / 2.0 * (passb[0] - passb[1]) +
                  math.sqrt(new_freq ** 2 * (passb[1] - passb[0]) ** 2 / 4.0 +
                       passb[1] * passb[0]))
        nat1 = passb[1] * passb[0] / nat0
        nat = xp.asarray([float(nat0), float(nat1)])
    elif filter_type == 4:
        nat0 = (1.0 / (2.0 * new_freq) * (passb[0] - passb[1]) +
                  math.sqrt((passb[1] - passb[0]) ** 2 / (4.0 * new_freq ** 2) +
                       passb[1] * passb[0]))
        nat1 = passb[0] * passb[1] / nat0
        nat = xp.asarray([float(nat0), float(nat1)])

    wn = _postprocess_wn(nat, analog, fs, xp=xp)

    return ord, wn


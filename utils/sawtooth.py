
def sawtooth(t, width=1.):
    """
    Return a periodic sawtooth or triangle waveform.

    The sawtooth waveform has a period ``2*pi``, rises from -1 to 1 on the
    interval 0 to ``width*2*pi``, then drops from 1 to -1 on the interval
    ``width*2*pi`` to ``2*pi``. `width` must be in the interval ``[0, 1]``.

    Note that this is not band-limited.  It produces an infinite number
    of harmonics, which are aliased back and forth across the frequency
    spectrum.

    Parameters
    ----------
    t : array_like
        Time.
    width : array_like, optional
        Width of the rising ramp as a proportion of the total cycle.
        Default is 1, producing a rising ramp, while 0 produces a falling
        ramp.  ``width=0.5`` produces a triangle wave.
        If an array, causes wave shape to change over time, and must be the
        same length as `t`.

    Returns
    -------
    y : ndarray
        Output array containing the sawtooth waveform.

    Examples
    --------
    A 5 Hz waveform sampled at 500 Hz for 1 second:

    >>> import numpy as np
    >>> from scipy import signal
    >>> import matplotlib.pyplot as plt
    >>> t = np.linspace(0, 1, 500)
    >>> plt.plot(t, signal.sawtooth(2 * np.pi * 5 * t))

    """
    xp = array_namespace(t, width)
    t, w = xp_promote(t, width, broadcast=True, force_floating=True, xp=xp)
    y = xp.zeros_like(t)

    # width must be between 0 and 1 inclusive
    mask1 = (w > 1) | (w < 0)
    y = xpx.at(y, mask1).set(xp.nan)

    # take t modulo 2*pi
    tmod = t % (2*xp.pi)

    # on the interval 0 to width*2*pi function is tmod / (pi*w) - 1
    mask2 = ~mask1 & (tmod < w*2*xp.pi)
    y = xpx.at(y, mask2).set(tmod[mask2]/(xp.pi*w[mask2]) - 1)

    # on the interval width*2*pi to 2*pi function is (pi*(w+1)-tmod) / (pi*(1-w))
    mask3 = ~(mask1 | mask2)
    y = xpx.at(y, mask3).set(
        (xp.pi*(w[mask3] + 1) - tmod[mask3])/(xp.pi*(1 - w[mask3]))
    )
    return y


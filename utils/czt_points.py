
def czt_points(m, w=None, a=1+0j):
    """
    Return the points at which the chirp z-transform is computed.

    Parameters
    ----------
    m : int
        The number of points desired.
    w : complex, optional
        The ratio between points in each step.
        Defaults to equally spaced points around the entire unit circle.
    a : complex, optional
        The starting point in the complex plane.  Default is 1+0j.

    Returns
    -------
    out : ndarray
        The points in the Z plane at which `CZT` samples the z-transform,
        when called with arguments `m`, `w`, and `a`, as complex numbers.

    See Also
    --------
    CZT : Class that creates a callable chirp z-transform function.
    czt : Convenience function for quickly calculating CZT.

    Examples
    --------
    Plot the points of a 16-point FFT:

    >>> import numpy as np
    >>> from scipy.signal import czt_points
    >>> points = czt_points(16)
    >>> import matplotlib.pyplot as plt
    >>> plt.plot(points.real, points.imag, 'o')
    >>> plt.gca().add_patch(plt.Circle((0,0), radius=1, fill=False, alpha=.3))
    >>> plt.axis('equal')
    >>> plt.show()

    and a 91-point logarithmic spiral that crosses the unit circle:

    >>> m, w, a = 91, 0.995*np.exp(-1j*np.pi*.05), 0.8*np.exp(1j*np.pi/6)
    >>> points = czt_points(m, w, a)
    >>> plt.plot(points.real, points.imag, 'o')
    >>> plt.gca().add_patch(plt.Circle((0,0), radius=1, fill=False, alpha=.3))
    >>> plt.axis('equal')
    >>> plt.show()
    """
    m = _validate_sizes(1, m)

    k = arange(m)

    a = 1.0 * a  # at least float

    if w is None:
        # Nothing specified, default to FFT
        return a * np.exp(2j * pi * k / m)
    else:
        # w specified
        w = 1.0 * w  # at least float
        return a * w**-k


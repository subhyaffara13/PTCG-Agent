
def getdomain(x):
    """
    Return a domain suitable for given abscissae.

    Find a domain suitable for a polynomial or Chebyshev series
    defined at the values supplied.

    Parameters
    ----------
    x : array_like
        1-d array of abscissae whose domain will be determined.

    Returns
    -------
    domain : ndarray
        1-d array containing two values.  If the inputs are complex, then
        the two returned points are the lower left and upper right corners
        of the smallest rectangle (aligned with the axes) in the complex
        plane containing the points `x`. If the inputs are real, then the
        two points are the ends of the smallest interval containing the
        points `x`.

    See Also
    --------
    mapparms, mapdomain

    Examples
    --------
    >>> import numpy as np
    >>> from numpy.polynomial import polyutils as pu
    >>> points = np.arange(4)**2 - 5; points
    array([-5, -4, -1,  4])
    >>> pu.getdomain(points)
    array([-5.,  4.])
    >>> c = np.exp(complex(0,1)*np.pi*np.arange(12)/6) # unit circle
    >>> pu.getdomain(c)
    array([-1.-1.j,  1.+1.j])

    """
    [x] = as_series([x], trim=False)
    if x.dtype.char in np.typecodes['Complex']:
        rmin, rmax = x.real.min(), x.real.max()
        imin, imax = x.imag.min(), x.imag.max()
        return np.array((complex(rmin, imin), complex(rmax, imax)))
    else:
        return np.array((x.min(), x.max()))


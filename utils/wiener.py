import math


def wiener(im, mysize=None, noise=None):
    """
    Perform a Wiener filter on an N-dimensional array.

    Apply a Wiener filter to the N-dimensional array `im`.

    Parameters
    ----------
    im : ndarray
        An N-dimensional array.
    mysize : int or array_like, optional
        A scalar or an N-length list giving the size of the Wiener filter
        window in each dimension.  Elements of mysize should be odd.
        If mysize is a scalar, then this scalar is used as the size
        in each dimension.
    noise : float, optional
        The noise-power to use. If None, then noise is estimated as the
        average of the local variance of the input.

    Returns
    -------
    out : ndarray
        Wiener filtered result with the same shape as `im`.

    Notes
    -----
    This implementation is similar to wiener2 in Matlab/Octave.
    For more details see [1]_

    References
    ----------
    .. [1] Lim, Jae S., Two-Dimensional Signal and Image Processing,
           Englewood Cliffs, NJ, Prentice Hall, 1990, p. 548.

    Examples
    --------
    >>> from scipy.datasets import face
    >>> from scipy.signal import wiener
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> rng = np.random.default_rng()
    >>> img = rng.random((40, 40))    #Create a random image
    >>> filtered_img = wiener(img, (5, 5))  #Filter the image
    >>> f, (plot1, plot2) = plt.subplots(1, 2)
    >>> plot1.imshow(img)
    >>> plot2.imshow(filtered_img)
    >>> plt.show()

    """
    xp = array_namespace(im)

    im = xp.asarray(im)
    if mysize is None:
        mysize = [3] * im.ndim
    mysize_arr = xp.asarray(mysize)
    if mysize_arr.shape == ():
        mysize = [mysize] * im.ndim

    # Estimate the local mean
    size = math.prod(mysize)
    lMean = correlate(im, xp.ones(mysize), 'same')
    lsize = float(size)
    lMean = lMean / lsize

    # Estimate the local variance
    lVar = (correlate(im ** 2, xp.ones(mysize), 'same') / lsize - lMean ** 2)

    # Estimate the noise power if needed.
    if noise is None:
        noise = xp.mean(xp.reshape(lVar, (-1,)), axis=0)

    res = (im - lMean)
    res *= (1 - noise / lVar)
    res += lMean
    out = xp.where(lVar < noise, lMean, res)

    return out


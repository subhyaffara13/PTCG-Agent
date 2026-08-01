
def hilbert2(x, N=None, axes=(-2, -1)):
    r"""Compute the '2-D' analytic signal of `x`.

    The 2-D analytic signal is calculated as a so-called "single-orthant" transform.
    This is achieved by applying one-dimensional Hilbert functions (as in
    `~scipy.signal.hilbert`) to the first and to the second array axis in Fourier space.

    For NumPy arrays, `scipy.fft.set_workers` can be used to change the number of
    workers used for the FFTs.

    Parameters
    ----------
    x : array_like
        Input signal. Must be at least two-dimensional.
    N : int or tuple of two ints, optional
        Number of output samples. `x` is initially cropped or zero-padded to length
        `N` along `axes`.  Default: ``x.shape[i] for i in axes``
    axes : tuple of two ints, optional
        Axes along which to do the transformation.  Default: (-2, -1).

        .. versionchanged:: 1.17

            Added `axes` parameter

    Returns
    -------
    xa : ndarray
        Analytic signal of `x` taken along given axes.

    Notes
    -----
    The "single-orthant" transform, as defined in [2]_, is calculated by performing the
    following steps:

    1. Calculate the two-dimensional FFT of the input, i.e.,

       .. math::

            X[p,q] = \sum_{k,l=0}^{N_0,N_1} x[k,l]\,
                                                 e^{-2j\pi k p/N_0}\, e^{-2j\pi l q/N_1}

    2. Zero negative frequency bins and double their positive counterparts, i.e.,

       .. math::

           X_a[p,q] = \big(1 + s_{N_0}(p)\big) \big(1 + s_{N_1}(q)\big) X[p,q]

       with :math:`s_N(.)` being a modified sign function defined as

       .. math::

           s_N(p) := \begin{cases}
                                 -1 & \text{ for } p < 0\ ,\\
                       \phantom{-}0 & \text{ for } p = 0\ ,\\
                                 +1 & \text{ for } 1 \leq p < (N+1) // 2\ ,\\
                       \phantom{-}0 & \text{ elsewhere.}
                     \end{cases}

       The limitation of the ":math:`+1`" case to the range of ``[1:(N+1)//2]``
       accounts for the unpaired Nyquist frequency bin at :math:`N/2` for even
       :math:`N`. Note that :math:`X_a[p] = \big(1 + s_N(p)\big) X[p]` is the
       one-dimensional Hilbert function (as in `~scipy.signal.hilbert`) in Fourier
       space.

    3. Produce the analytic signal by performing the inverse FFT, i.e.,

       .. math::

           x_a[k, l] = \frac{1}{N_0 N_1}
                 \sum_{p,q=0}^{N_0,N_1} X_a[p,q]\, e^{2j\pi k p/N_0}\, e^{2j\pi l q/N_1}

    The "single-orthant" transform is not the only possible definition of an analytic
    signal in multiple dimensions (as noted in [1]_). Consult [3]_ for a description of
    properties that this 2-D transform does and does not share with the 1-D transform.
    The second example below shows one of the downsides of this approach.

    References
    ----------
    .. [1] Wikipedia, "Analytic signal",
        https://en.wikipedia.org/wiki/Analytic_signal
    .. [2] Hahn, Stefan L. "Multidimensional complex signals with
        single-orthant spectra." Proceedings of the IEEE 80.8
        (1992): 1287-1300.
        `PDF <https://ieeexplore.ieee.org/iel1/5/4083/00158601.pdf>`__
    .. [3] Bülow, Thomas, and Gerald Sommer. "A novel approach to the 2D analytic
        signal." In International Conference on Computer Analysis of Images and
        Patterns, pp. 25-32. Berlin, Heidelberg: Springer Berlin Heidelberg, 1999.
        `PDF <https://www.informatik.uni-kiel.de/inf/Sommer/doc/Publications/tbl/caip99.pdf>`__

    Examples
    --------
    The following example calculates the two-dimensional analytic signal from a single
    impulse with an added constant offset. The impulse produces an FFT where each bin
    has a value of one and the constant offset component produces only a non-zero
    component at the ``(0,0)`` bin.

    >>> import numpy as np
    >>> from scipy.fft import fft2, fftshift, ifftshift
    >>> from scipy.signal import hilbert2
    ...
    >>> # Input signal is unit impulse with a constant offset:
    >>> x = np.ones((5, 5)) / 5
    >>> x[0, 0] += 1
    ...
    >>> X = fftshift(fft2(x))  # Zero frequency bin is at center
    >>> print(X)
    [[1.-0.j 1.-0.j 1.-0.j 1.+0.j 1.+0.j]
     [1.-0.j 1.-0.j 1.-0.j 1.+0.j 1.+0.j]
     [1.-0.j 1.-0.j 6.-0.j 1.+0.j 1.+0.j]
     [1.-0.j 1.-0.j 1.+0.j 1.+0.j 1.+0.j]
     [1.-0.j 1.-0.j 1.+0.j 1.+0.j 1.+0.j]]
    >>> x_a = hilbert2(x)
    >>> X_a = fftshift(fft2(x_a))
    >>> print(np.round(X_a, 3))
    [[ 0.+0.j  0.+0.j -0.+0.j  0.+0.j  0.+0.j]
     [ 0.+0.j  0.+0.j -0.+0.j  0.+0.j  0.+0.j]
     [ 0.+0.j  0.+0.j  6.+0.j  2.+0.j  2.+0.j]
     [ 0.+0.j  0.+0.j  2.+0.j  4.+0.j  4.+0.j]
     [ 0.+0.j  0.+0.j  2.+0.j  4.+0.j  4.+0.j]]

    The FFT of the result illustrates that the values of the lower right quadrant (or
    orthant) with purely positive frequency bins have been quadrupled. The values at its
    borders, where only one frequency component is zero, are doubled. The zero frequency
    bin ``(0, 0)`` has not been altered. All other quadrants have been set to zero.

    This second example illustrates a problem with the "single-orthant" convention. A
    purely real signal can produce an analytic signal which is completely zero:

    >>> from scipy.fft import fft2, fftshift, ifft2, ifftshift
    >>> from scipy.signal import hilbert2
    ...
    >>> # Create a real signal by ensuring `Z[-p,-q] == np.conj(Z[p,q])` holds:
    >>> Z = np.array([[0, 0, 0, 0, 0],
    ...               [0, 0, 0, 1, 0],
    ...               [0, 0, 0, 0, 0],
    ...               [0, 1, 0, 0, 0],
    ...               [0, 0, 0, 0, 0]]) * 25
    >>> z = ifft2(ifftshift(Z))
    >>> np.allclose(z.imag, 0)  # z is a real signal
    True
    >>> np.sum(z.real**2)  # z.real is non-zero
    np.float64(50.0)
    >>> z_a = hilbert2(z.real)
    >>> np.allclose(z_a, 0)  # analytic signal is zero
    True

    """
    xp = array_namespace(x)
    x = xpx.atleast_nd(xp.asarray(x), ndim=2, xp=xp)
    if xp.isdtype(x.dtype, 'complex floating'):
        raise ValueError("x must be real.")
    if len(axes) != 2:
        raise ValueError("axes must be a tuple of length 2")
    if axes[0] == axes[1]:
        raise ValueError("axes must contain 2 distinct axes")

    if N is None:
        N = (x.shape[axes[0]], x.shape[axes[1]])
    elif isinstance(N, int):
        if N <= 0:
            raise ValueError("N must be positive.")
        N = (N, N)
    elif len(N) != 2 or np.any(np.asarray(N) <= 0):
        raise ValueError("When given as a tuple, N must hold exactly "
                         "two positive integers")

    Xf = sp_fft.fft2(x, N, axes=axes)
    Xf = xp.moveaxis(Xf, axes, (-2, -1))
    k0, k1 = (N[0] + 1) // 2, (N[1] + 1) // 2

    if k0 > 1:  # condition k0 > 1 needed for Dask backend
        Xf = xpx.at(Xf)[..., 1:k0, :].multiply(2.0)
    if k1 > 1:  # condition k1 > 1 needed for Dask backend
        Xf = xpx.at(Xf)[..., :, 1:k1].multiply(2.0)
    Xf = xpx.at(Xf)[..., k0:, :].set(0.0)
    Xf = xpx.at(Xf)[..., :, k1:].set(0.0)

    Xf = xp.moveaxis(Xf, (-2, -1), axes)
    x = sp_fft.ifft2(Xf, axes=axes)
    return x


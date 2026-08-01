
def spline_filter(input, order=3, output=np.float64, mode='mirror'):
    """
    Multidimensional spline filter.

    Parameters
    ----------
    %(input)s
    order : int, optional
        The order of the spline, default is 3.
    output : ndarray or dtype, optional
        The array in which to place the output, or the dtype of the returned
        array. Default is ``numpy.float64``.
    %(mode_interp_mirror)s

    Returns
    -------
    spline_filter : ndarray
        Filtered array. Has the same shape as `input`.

    See Also
    --------
    spline_filter1d : Calculate a 1-D spline filter along the given axis.

    Notes
    -----
    The multidimensional filter is implemented as a sequence of
    1-D spline filters. The intermediate arrays are stored
    in the same data type as the output. Therefore, for output types
    with a limited precision, the results may be imprecise because
    intermediate results may be stored with insufficient precision.

    For complex-valued `input`, this function processes the real and imaginary
    components independently.

    .. versionadded:: 1.6.0
        Complex-valued support added.

    Examples
    --------
    We can filter an image using multidimensional splines:

    >>> from scipy.ndimage import spline_filter
    >>> import numpy as np
    >>> import matplotlib.pyplot as plt
    >>> orig_img = np.eye(20)  # create an image
    >>> orig_img[10, :] = 1.0
    >>> sp_filter = spline_filter(orig_img, order=3)
    >>> f, ax = plt.subplots(1, 2, sharex=True)
    >>> for ind, data in enumerate([[orig_img, "original image"],
    ...                             [sp_filter, "spline filter"]]):
    ...     ax[ind].imshow(data[0], cmap='gray_r')
    ...     ax[ind].set_title(data[1])
    >>> plt.tight_layout()
    >>> plt.show()

    """
    if order < 2 or order > 5:
        raise RuntimeError('spline order not supported')
    input = np.asarray(input)
    complex_output = np.iscomplexobj(input)
    output = _ni_support._get_output(output, input,
                                     complex_output=complex_output)
    if complex_output:
        spline_filter(input.real, order, output.real, mode)
        spline_filter(input.imag, order, output.imag, mode)
        return output
    if order not in [0, 1] and input.ndim > 0:
        for axis in range(input.ndim):
            spline_filter1d(input, order, axis, output=output, mode=mode)
            input = output
    else:
        output[...] = input[...]
    return output


def spline_filter(Iin, lmbda=5.0):
    """Smoothing spline (cubic) filtering of a rank-2 array.

    Filter an input data set, `Iin`, using a (cubic) smoothing spline of
    fall-off `lmbda`.

    Parameters
    ----------
    Iin : array_like
        input data set
    lmbda : float, optional
        spline smoothing fall-off value, default is `5.0`.

    Returns
    -------
    res : ndarray
        filtered input data

    Examples
    --------
    We can filter an multi dimensional signal (ex: 2D image) using cubic
    B-spline filter:

    >>> import numpy as np
    >>> from scipy.signal import spline_filter
    >>> import matplotlib.pyplot as plt
    >>> orig_img = np.eye(20)  # create an image
    >>> orig_img[10, :] = 1.0
    >>> sp_filter = spline_filter(orig_img, lmbda=0.1)
    >>> f, ax = plt.subplots(1, 2, sharex=True)
    >>> for ind, data in enumerate([[orig_img, "original image"],
    ...                             [sp_filter, "spline filter"]]):
    ...     ax[ind].imshow(data[0], cmap='gray_r')
    ...     ax[ind].set_title(data[1])
    >>> plt.tight_layout()
    >>> plt.show()

    """
    xp = array_namespace(Iin)
    Iin = np.asarray(Iin)

    if Iin.dtype not in [np.float32, np.float64, np.complex64, np.complex128]:
        raise TypeError(f"Invalid data type for Iin: {Iin.dtype = }")

    # XXX: note that complex-valued computations are done in single precision
    # this is historic, and the root reason is unclear,
    # see https://github.com/scipy/scipy/issues/9209
    # Attempting to work in complex double precision leads to symiirorder1
    # failing to converge for the boundary conditions.
    intype = Iin.dtype
    hcol = array([1.0, 4.0, 1.0], np.float32) / 6.0
    if intype == np.complex128:
        Iin = Iin.astype(np.complex64)

    ck = cspline2d(Iin, lmbda)
    out = sepfir2d(ck, hcol, hcol)
    out = out.astype(intype)
    return xp.asarray(out)


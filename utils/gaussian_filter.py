
def gaussian_filter(input, sigma, order=0, output=None,
                    mode="reflect", cval=0.0, truncate=4.0, *, radius=None,
                    axes=None):
    """Multidimensional Gaussian filter.

    Parameters
    ----------
    %(input)s
    sigma : scalar or sequence of scalars
        Standard deviation for Gaussian kernel. The standard
        deviations of the Gaussian filter are given for each axis as a
        sequence, or as a single number, in which case it is equal for
        all axes.
    order : int or sequence of ints, optional
        The order of the filter along each axis is given as a sequence
        of integers, or as a single number. An order of 0 corresponds
        to convolution with a Gaussian kernel. A positive order
        corresponds to convolution with that derivative of a Gaussian.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    truncate : float, optional
        Truncate the filter at this many standard deviations.
        Default is 4.0.
    radius : None or int or sequence of ints, optional
        Radius of the Gaussian kernel. The radius are given for each axis
        as a sequence, or as a single number, in which case it is equal
        for all axes. If specified, the size of the kernel along each axis
        will be ``2*radius + 1``, and `truncate` is ignored.
        Default is None.
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `sigma`, `order`, `mode` and/or `radius`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    gaussian_filter : ndarray
        Returned array of same shape as `input`.

    Notes
    -----
    The multidimensional filter is implemented as a sequence of
    1-D convolution filters. The intermediate arrays are
    stored in the same data type as the output. Therefore, for output
    types with a limited precision, the results may be imprecise
    because intermediate results may be stored with insufficient
    precision.

    The Gaussian kernel will have size ``2*radius + 1`` along each axis. If
    `radius` is None, the default ``radius = round(truncate * sigma)`` will be
    used.

    Examples
    --------
    >>> from scipy.ndimage import gaussian_filter
    >>> import numpy as np
    >>> a = np.arange(50, step=2).reshape((5,5))
    >>> a
    array([[ 0,  2,  4,  6,  8],
           [10, 12, 14, 16, 18],
           [20, 22, 24, 26, 28],
           [30, 32, 34, 36, 38],
           [40, 42, 44, 46, 48]])
    >>> gaussian_filter(a, sigma=1)
    array([[ 4,  6,  8,  9, 11],
           [10, 12, 14, 15, 17],
           [20, 22, 24, 25, 27],
           [29, 31, 33, 34, 36],
           [35, 37, 39, 40, 42]])

    >>> from scipy import datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = gaussian_filter(ascent, sigma=5)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    input = np.asarray(input)
    output = _ni_support._get_output(output, input)

    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    orders = _ni_support._normalize_sequence(order, num_axes)
    sigmas = _ni_support._normalize_sequence(sigma, num_axes)
    modes = _ni_support._normalize_sequence(mode, num_axes)
    radiuses = _ni_support._normalize_sequence(radius, num_axes)
    axes = [(axes[ii], sigmas[ii], orders[ii], modes[ii], radiuses[ii])
            for ii in range(num_axes) if sigmas[ii] > 1e-15]
    if len(axes) > 0:
        for axis, sigma, order, mode, radius in axes:
            gaussian_filter1d(input, sigma, axis, order, output,
                              mode, cval, truncate, radius=radius)
            input = output
    else:
        output[...] = input[...]
    return output


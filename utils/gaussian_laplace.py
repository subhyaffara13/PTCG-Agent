
def gaussian_laplace(input, sigma, output=None, mode="reflect",
                     cval=0.0, *, axes=None, **kwargs):
    """Multidimensional Laplace filter using Gaussian second derivatives.

    Parameters
    ----------
    %(input)s
    sigma : scalar or sequence of scalars
        The standard deviations of the Gaussian filter are given for
        each axis as a sequence, or as a single number, in which case
        it is equal for all axes.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    axes : tuple of int or None
        The axes over which to apply the filter. If `sigma` or `mode` tuples
        are provided, their length must match the number of axes.
    **kwargs
        Extra keyword arguments will be passed to `gaussian_filter`.

    Returns
    -------
    gaussian_laplace : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> ascent = datasets.ascent()

    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side

    >>> result = ndimage.gaussian_laplace(ascent, sigma=1)
    >>> ax1.imshow(result)

    >>> result = ndimage.gaussian_laplace(ascent, sigma=3)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    input = np.asarray(input)

    def derivative2(input, axis, output, mode, cval, sigma, **kwargs):
        order = [0] * input.ndim
        order[axis] = 2
        return gaussian_filter(input, sigma, order, output, mode, cval,
                               **kwargs)

    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    sigma = _ni_support._normalize_sequence(sigma, num_axes)
    if num_axes < input.ndim:
        # set sigma = 0 for any axes not being filtered
        sigma_temp = [0,] * input.ndim
        for s, ax in zip(sigma, axes):
            sigma_temp[ax] = s
        sigma = sigma_temp

    return generic_laplace(input, derivative2, output, mode, cval,
                           extra_arguments=(sigma,),
                           extra_keywords=kwargs,
                           axes=axes)


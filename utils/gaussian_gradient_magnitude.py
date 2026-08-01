
def gaussian_gradient_magnitude(input, sigma, output=None,
                                mode="reflect", cval=0.0, *, axes=None,
                                **kwargs):
    """Multidimensional gradient magnitude using Gaussian derivatives.

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
    gaussian_gradient_magnitude : ndarray
        Filtered array. Has the same shape as `input`.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.gaussian_gradient_magnitude(ascent, sigma=5)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    input = np.asarray(input)

    def derivative(input, axis, output, mode, cval, sigma, **kwargs):
        order = [0] * input.ndim
        order[axis] = 1
        return gaussian_filter(input, sigma, order, output, mode,
                               cval, **kwargs)

    return generic_gradient_magnitude(input, derivative, output, mode,
                                      cval, extra_arguments=(sigma,),
                                      extra_keywords=kwargs, axes=axes)


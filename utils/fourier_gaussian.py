
def fourier_gaussian(input, sigma, n=-1, axis=-1, output=None):
    """
    Multidimensional Gaussian fourier filter.

    The array is multiplied with the fourier transform of a Gaussian
    kernel.

    Parameters
    ----------
    input : array_like
        The input array.
    sigma : float or sequence
        The sigma of the Gaussian kernel. If a float, `sigma` is the same for
        all axes. If a sequence, `sigma` has to contain one value for each
        axis.
    n : int, optional
        If `n` is negative (default), then the input is assumed to be the
        result of a complex fft.
        If `n` is larger than or equal to zero, the input is assumed to be the
        result of a real fft, and `n` gives the length of the array before
        transformation along the real transform direction.
    axis : int, optional
        The axis of the real transform.
    output : ndarray, optional
        If given, the result of filtering the input is placed in this array.

    Returns
    -------
    fourier_gaussian : ndarray
        The filtered input.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import numpy.fft
    >>> import matplotlib.pyplot as plt
    >>> fig, (ax1, ax2) = plt.subplots(1, 2)
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ascent = datasets.ascent()
    >>> input_ = numpy.fft.fft2(ascent)
    >>> result = ndimage.fourier_gaussian(input_, sigma=4)
    >>> result = numpy.fft.ifft2(result)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result.real)  # the imaginary part is an artifact
    >>> plt.show()
    """
    input = np.asarray(input)
    output = _get_output_fourier(output, input)
    axis = normalize_axis_index(axis, input.ndim)
    sigmas = _ni_support._normalize_sequence(sigma, input.ndim)
    sigmas = np.asarray(sigmas, dtype=np.float64)
    if not sigmas.flags.contiguous:
        sigmas = sigmas.copy()

    _nd_image.fourier_filter(input, sigmas, n, axis, output, 0)
    return output


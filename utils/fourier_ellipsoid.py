
def fourier_ellipsoid(input, size, n=-1, axis=-1, output=None):
    """
    Multidimensional ellipsoid Fourier filter.

    The array is multiplied with the fourier transform of an ellipsoid of
    given sizes.

    Parameters
    ----------
    input : array_like
        The input array.
    size : float or sequence
        The size of the box used for filtering.
        If a float, `size` is the same for all axes. If a sequence, `size` has
        to contain one value for each axis.
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
    fourier_ellipsoid : ndarray
        The filtered input.

    Notes
    -----
    This function is implemented for arrays of rank 1, 2, or 3.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import numpy.fft
    >>> import matplotlib.pyplot as plt
    >>> fig, (ax1, ax2) = plt.subplots(1, 2)
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ascent = datasets.ascent()
    >>> input_ = numpy.fft.fft2(ascent)
    >>> result = ndimage.fourier_ellipsoid(input_, size=20)
    >>> result = numpy.fft.ifft2(result)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result.real)  # the imaginary part is an artifact
    >>> plt.show()
    """
    input = np.asarray(input)
    if input.ndim > 3:
        raise NotImplementedError("Only 1d, 2d and 3d inputs are supported")
    output = _get_output_fourier(output, input)
    if output.size == 0:
        # The C code has a bug that can result in a segfault with arrays
        # that have size 0 (gh-17270), so check here.
        return output
    axis = normalize_axis_index(axis, input.ndim)
    sizes = _ni_support._normalize_sequence(size, input.ndim)
    sizes = np.asarray(sizes, dtype=np.float64)
    if not sizes.flags.contiguous:
        sizes = sizes.copy()
    _nd_image.fourier_filter(input, sizes, n, axis, output, 2)
    return output


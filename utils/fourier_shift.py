
def fourier_shift(input, shift, n=-1, axis=-1, output=None):
    """
    Multidimensional Fourier shift filter.

    The array is multiplied with the Fourier transform of a shift operation.

    Parameters
    ----------
    input : array_like
        The input array.
    shift : float or sequence
        The size of the box used for filtering.
        If a float, `shift` is the same for all axes. If a sequence, `shift`
        has to contain one value for each axis.
    n : int, optional
        If `n` is negative (default), then the input is assumed to be the
        result of a complex fft.
        If `n` is larger than or equal to zero, the input is assumed to be the
        result of a real fft, and `n` gives the length of the array before
        transformation along the real transform direction.
    axis : int, optional
        The axis of the real transform.
    output : ndarray, optional
        If given, the result of shifting the input is placed in this array.

    Returns
    -------
    fourier_shift : ndarray
        The shifted input.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> import numpy.fft
    >>> fig, (ax1, ax2) = plt.subplots(1, 2)
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ascent = datasets.ascent()
    >>> input_ = numpy.fft.fft2(ascent)
    >>> result = ndimage.fourier_shift(input_, shift=200)
    >>> result = numpy.fft.ifft2(result)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result.real)  # the imaginary part is an artifact
    >>> plt.show()
    """
    input = np.asarray(input)
    output = _get_output_fourier_complex(output, input)
    axis = normalize_axis_index(axis, input.ndim)
    shifts = _ni_support._normalize_sequence(shift, input.ndim)
    shifts = np.asarray(shifts, dtype=np.float64)
    if not shifts.flags.contiguous:
        shifts = shifts.copy()
    _nd_image.fourier_shift(input, shifts, n, axis, output)
    return output


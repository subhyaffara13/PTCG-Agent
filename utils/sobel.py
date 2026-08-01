
def sobel(input, axis=-1, output=None, mode="reflect", cval=0.0):
    """Calculate a Sobel filter.

    Parameters
    ----------
    %(input)s
    %(axis)s
    %(output)s
    %(mode_multiple)s
    %(cval)s

    Returns
    -------
    sobel : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    This function computes the axis-specific Sobel gradient.
    The horizontal edges can be emphasised with the horizontal transform (axis=0),
    the vertical edges with the vertical transform (axis=1) and so on for higher
    dimensions. These can be combined to give the magnitude.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> ascent = datasets.ascent().astype('int32')
    >>> sobel_h = ndimage.sobel(ascent, 0)  # horizontal gradient
    >>> sobel_v = ndimage.sobel(ascent, 1)  # vertical gradient
    >>> magnitude = np.sqrt(sobel_h**2 + sobel_v**2)
    >>> magnitude *= 255.0 / np.max(magnitude)  # normalization
    >>> fig, axs = plt.subplots(2, 2, figsize=(8, 8))
    >>> plt.gray()  # show the filtered result in grayscale
    >>> axs[0, 0].imshow(ascent)
    >>> axs[0, 1].imshow(sobel_h)
    >>> axs[1, 0].imshow(sobel_v)
    >>> axs[1, 1].imshow(magnitude)
    >>> titles = ["original", "horizontal", "vertical", "magnitude"]
    >>> for i, ax in enumerate(axs.ravel()):
    ...     ax.set_title(titles[i])
    ...     ax.axis("off")
    >>> plt.show()

    """
    input = np.asarray(input)
    axis = normalize_axis_index(axis, input.ndim)
    output = _ni_support._get_output(output, input)
    modes = _ni_support._normalize_sequence(mode, input.ndim)
    correlate1d(input, [-1, 0, 1], axis, output, modes[axis], cval, 0)
    axes = [ii for ii in range(input.ndim) if ii != axis]
    for ii in axes:
        correlate1d(output, [1, 2, 1], ii, output, modes[ii], cval, 0)
    return output



def prewitt(input, axis=-1, output=None, mode="reflect", cval=0.0):
    """Calculate a Prewitt filter.

    Parameters
    ----------
    %(input)s
    %(axis)s
    %(output)s
    %(mode_multiple)s
    %(cval)s

    Returns
    -------
    prewitt : ndarray
        Filtered array. Has the same shape as `input`.

    See Also
    --------
    sobel: Sobel filter

    Notes
    -----
    This function computes the one-dimensional Prewitt filter.
    Horizontal edges are emphasised with the horizontal transform (axis=0),
    vertical edges with the vertical transform (axis=1), and so on for higher
    dimensions. These can be combined to give the magnitude.

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> ascent = datasets.ascent()
    >>> prewitt_h = ndimage.prewitt(ascent, axis=0)
    >>> prewitt_v = ndimage.prewitt(ascent, axis=1)
    >>> magnitude = np.sqrt(prewitt_h ** 2 + prewitt_v ** 2)
    >>> magnitude *= 255 / np.max(magnitude) # Normalization
    >>> fig, axes = plt.subplots(2, 2, figsize = (8, 8))
    >>> plt.gray()
    >>> axes[0, 0].imshow(ascent)
    >>> axes[0, 1].imshow(prewitt_h)
    >>> axes[1, 0].imshow(prewitt_v)
    >>> axes[1, 1].imshow(magnitude)
    >>> titles = ["original", "horizontal", "vertical", "magnitude"]
    >>> for i, ax in enumerate(axes.ravel()):
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
        correlate1d(output, [1, 1, 1], ii, output, modes[ii], cval, 0,)
    return output


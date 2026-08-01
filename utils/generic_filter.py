
def generic_filter(input, function, size=None, footprint=None,
                   output=None, mode="reflect", cval=0.0, origin=0,
                   extra_arguments=(), extra_keywords=None, *, axes=None):
    """Calculate a multidimensional filter using the given function.

    At each element the provided function is called. The input values
    within the filter footprint at that element are passed to the function
    as a 1-D array of double values.

    Parameters
    ----------
    %(input)s
    function : {callable, scipy.LowLevelCallable}
        Function to apply at each element.
    %(size_foot)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin_multiple)s
    %(extra_arguments)s
    %(extra_keywords)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `size` or `origin` must match the length
        of `axes`. The ith entry in any of these tuples corresponds to the ith
        entry in `axes`.

    Returns
    -------
    output : ndarray
        Filtered array. Has the same shape as `input`.

    See Also
    --------
    vectorized_filter : similar functionality, but optimized for vectorized callables

    Notes
    -----
    This function is ideal for use with instances of `scipy.LowLevelCallable`;
    for vectorized, pure-Python callables, consider `vectorized_filter` for improved
    performance.

    Low-level callback functions must have one of the following signatures:

    .. code:: c

       int callback(double *buffer, npy_intp filter_size,
                    double *return_value, void *user_data)
       int callback(double *buffer, intptr_t filter_size,
                    double *return_value, void *user_data)

    The calling function iterates over the elements of the input and
    output arrays, calling the callback function at each element. The
    elements within the footprint of the filter at the current element are
    passed through the ``buffer`` parameter, and the number of elements
    within the footprint through ``filter_size``. The calculated value is
    returned in ``return_value``. ``user_data`` is the data pointer provided
    to `scipy.LowLevelCallable` as-is.

    The callback function must return an integer error status that is zero
    if something went wrong and one otherwise. If an error occurs, you should
    normally set the python error status with an informative message
    before returning, otherwise a default error message is set by the
    calling function.

    In addition, some other low-level function pointer specifications
    are accepted, but these are for backward compatibility only and should
    not be used in new code.

    Examples
    --------
    Import the necessary modules and load the example image used for
    filtering.

    >>> import numpy as np
    >>> from scipy import datasets
    >>> from scipy.ndimage import zoom, generic_filter
    >>> import matplotlib.pyplot as plt
    >>> ascent = zoom(datasets.ascent(), 0.5)

    Compute a maximum filter with kernel size 5 by passing a simple NumPy
    aggregation function as argument to `function`.

    >>> maximum_filter_result = generic_filter(ascent, np.amax, [5, 5])

    While a maximum filter could also directly be obtained using
    `maximum_filter`, `generic_filter` allows generic Python function or
    `scipy.LowLevelCallable` to be used as a filter. Here, we compute the
    range between maximum and minimum value as an example for a kernel size
    of 5.

    >>> def custom_filter(image):
    ...     return np.amax(image) - np.amin(image)
    >>> custom_filter_result = generic_filter(ascent, custom_filter, [5, 5])

    Plot the original and filtered images.

    >>> fig, axes = plt.subplots(3, 1, figsize=(3, 9))
    >>> plt.gray()  # show the filtered result in grayscale
    >>> top, middle, bottom = axes
    >>> for ax in axes:
    ...     ax.set_axis_off()  # remove coordinate system
    >>> top.imshow(ascent)
    >>> top.set_title("Original image")
    >>> middle.imshow(maximum_filter_result)
    >>> middle.set_title("Maximum filter, Kernel: 5x5")
    >>> bottom.imshow(custom_filter_result)
    >>> bottom.set_title("Custom filter, Kernel: 5x5")
    >>> fig.tight_layout()

    """
    if (size is not None) and (footprint is not None):
        warnings.warn("ignoring size because footprint is set",
                      UserWarning, stacklevel=2)
    if extra_keywords is None:
        extra_keywords = {}
    input = np.asarray(input)
    if np.iscomplexobj(input):
        raise TypeError('Complex type not supported')
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if footprint is None:
        if size is None:
            raise RuntimeError("no footprint or filter size provided")
        sizes = _ni_support._normalize_sequence(size, num_axes)
        footprint = np.ones(sizes, dtype=bool)
    else:
        footprint = np.asarray(footprint, dtype=bool)

    # expand origins, footprint if num_axes < input.ndim
    footprint = _expand_footprint(input.ndim, axes, footprint)
    origins = _expand_origin(input.ndim, axes, origin)

    fshape = [ii for ii in footprint.shape if ii > 0]
    if len(fshape) != input.ndim:
        raise RuntimeError(f"footprint.ndim ({footprint.ndim}) "
                           f"must match len(axes) ({num_axes})")
    for origin, lenf in zip(origins, fshape):
        if (lenf // 2 + origin < 0) or (lenf // 2 + origin >= lenf):
            raise ValueError('invalid origin')
    if not footprint.flags.contiguous:
        footprint = footprint.copy()
    output = _ni_support._get_output(output, input)

    mode = _ni_support._extend_mode_to_code(mode)
    _nd_image.generic_filter(input, function, footprint, output, mode,
                             cval, origins, extra_arguments, extra_keywords)
    return output


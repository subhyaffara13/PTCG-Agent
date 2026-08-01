
def generic_filter1d(input, function, filter_size, axis=-1,
                     output=None, mode="reflect", cval=0.0, origin=0,
                     extra_arguments=(), extra_keywords=None):
    """Calculate a 1-D filter along the given axis.

    `generic_filter1d` iterates over the lines of the array, calling the
    given function at each line. The arguments of the line are the
    input line, and the output line. The input and output lines are 1-D
    double arrays. The input line is extended appropriately according
    to the filter size and origin. The output line must be modified
    in-place with the result.

    Parameters
    ----------
    %(input)s
    function : {callable, scipy.LowLevelCallable}
        Function to apply along given axis.
    filter_size : scalar
        Length of the filter.
    %(axis)s
    %(output)s
    %(mode_reflect)s
    %(cval)s
    %(origin)s
    %(extra_arguments)s
    %(extra_keywords)s

    Returns
    -------
    generic_filter1d : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    This function also accepts low-level callback functions with one of
    the following signatures and wrapped in `scipy.LowLevelCallable`:

    .. code:: c

       int function(double *input_line, npy_intp input_length,
                    double *output_line, npy_intp output_length,
                    void *user_data)
       int function(double *input_line, intptr_t input_length,
                    double *output_line, intptr_t output_length,
                    void *user_data)

    The calling function iterates over the lines of the input and output
    arrays, calling the callback function at each line. The current line
    is extended according to the border conditions set by the calling
    function, and the result is copied into the array that is passed
    through ``input_line``. The length of the input line (after extension)
    is passed through ``input_length``. The callback function should apply
    the filter and store the result in the array passed through
    ``output_line``. The length of the output line is passed through
    ``output_length``. ``user_data`` is the data pointer provided
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
    This example defines and applies a custom callback function that computes
    the range (maximum minus minimum) within a sliding window of size 3.
    It utilizes `numpy.lib.stride_tricks.sliding_window_view` and demonstrates the
    required in-place modification of the ``output_line`` array.

    >>> import numpy as np
    >>> from scipy.ndimage import generic_filter1d
    >>> from numpy.lib.stride_tricks import sliding_window_view

    >>> def local_range(input_line, output_line):
    ...     # input_line includes padded values according to `filter_size` and `mode`
    ...     v = sliding_window_view(input_line, 3)
    ...     # modify `output_line` in-place rather than returning the result
    ...     output_line[:] = v.max(axis=1) - v.min(axis=1)

    >>> x = np.array([1, 2, 3, 4, 5], dtype=np.float64)
    >>> generic_filter1d(x, local_range, filter_size=3)
    array([1., 2., 2., 2., 1.])

    """
    if extra_keywords is None:
        extra_keywords = {}
    input = np.asarray(input)
    if np.iscomplexobj(input):
        raise TypeError('Complex type not supported')
    output = _ni_support._get_output(output, input)
    if filter_size < 1:
        raise RuntimeError('invalid filter size')
    axis = normalize_axis_index(axis, input.ndim)
    if (filter_size // 2 + origin < 0) or (filter_size // 2 + origin >=
                                           filter_size):
        raise ValueError('invalid origin')
    mode = _ni_support._extend_mode_to_code(mode)
    _nd_image.generic_filter1d(input, function, filter_size, axis, output,
                               mode, cval, origin, extra_arguments,
                               extra_keywords)
    return output


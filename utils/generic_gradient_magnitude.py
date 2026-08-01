
def generic_gradient_magnitude(input, derivative, output=None,
                               mode="reflect", cval=0.0,
                               extra_arguments=(), extra_keywords=None,
                               *, axes=None):
    """Gradient magnitude using a provided gradient function.

    Parameters
    ----------
    %(input)s
    derivative : callable
        Callable with the following signature::

            derivative(input, axis, output, mode, cval,
                       *extra_arguments, **extra_keywords)

        See `extra_arguments`, `extra_keywords` below.
        `derivative` can assume that `input` and `output` are ndarrays.
        Note that the output from `derivative` is modified inplace;
        be careful to copy important inputs before returning them.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(extra_arguments)s
    %(extra_keywords)s
    axes : tuple of int or None
        The axes over which to apply the filter. If a `mode` tuple is
        provided, its length must match the number of axes.

    Returns
    -------
    generic_gradient_magnitude : ndarray
        Filtered array. Has the same shape as `input`.

    """
    if extra_keywords is None:
        extra_keywords = {}
    input = np.asarray(input)
    output = _ni_support._get_output(output, input)
    axes = _ni_support._check_axes(axes, input.ndim)
    if len(axes) > 0:
        modes = _ni_support._normalize_sequence(mode, len(axes))
        derivative(input, axes[0], output, modes[0], cval,
                   *extra_arguments, **extra_keywords)
        np.multiply(output, output, output)
        for ii in range(1, len(axes)):
            tmp = derivative(input, axes[ii], output.dtype, modes[ii], cval,
                             *extra_arguments, **extra_keywords)
            np.multiply(tmp, tmp, tmp)
            output += tmp
        # This allows the sqrt to work with a different default casting
        np.sqrt(output, output, casting='unsafe')
    else:
        output[...] = input[...]
    return output


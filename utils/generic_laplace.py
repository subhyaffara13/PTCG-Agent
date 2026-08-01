
def generic_laplace(input, derivative2, output=None, mode="reflect",
                    cval=0.0,
                    extra_arguments=(),
                    extra_keywords=None,
                    *, axes=None):
    """
    N-D Laplace filter using a provided second derivative function.

    Parameters
    ----------
    %(input)s
    derivative2 : callable
        Callable with the following signature::

            derivative2(input, axis, output, mode, cval,
                        *extra_arguments, **extra_keywords)

        See `extra_arguments`, `extra_keywords` below.
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
    generic_laplace : ndarray
        Filtered array. Has the same shape as `input`.

    """
    if extra_keywords is None:
        extra_keywords = {}
    input = np.asarray(input)
    output = _ni_support._get_output(output, input)
    axes = _ni_support._check_axes(axes, input.ndim)
    if len(axes) > 0:
        modes = _ni_support._normalize_sequence(mode, len(axes))
        derivative2(input, axes[0], output, modes[0], cval,
                    *extra_arguments, **extra_keywords)
        for ii in range(1, len(axes)):
            tmp = derivative2(input, axes[ii], output.dtype, modes[ii], cval,
                              *extra_arguments, **extra_keywords)
            output += tmp
    else:
        output[...] = input[...]
    return output


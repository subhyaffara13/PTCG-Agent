
def choose_conv_method(in1, in2, mode='full', measure=False):
    """
    Find the fastest convolution/correlation method.

    This primarily exists to be called during the ``method='auto'`` option in
    `convolve` and `correlate`. It can also be used to determine the value of
    ``method`` for many different convolutions of the same dtype/shape.
    In addition, it supports timing the convolution to adapt the value of
    ``method`` to a particular set of inputs and/or hardware.

    Parameters
    ----------
    in1 : array_like
        The first argument passed into the convolution function.
    in2 : array_like
        The second argument passed into the convolution function.
    mode : str {'full', 'valid', 'same'}, optional
        A string indicating the size of the output:

        ``full``
           The output is the full discrete linear convolution
           of the inputs. (Default)
        ``valid``
           The output consists only of those elements that do not
           rely on the zero-padding.
        ``same``
           Output size will be ``N``, the same size as `in1`, centered
           with respect to the 'full' output.
           Boundary effects may be visible.
    measure : bool, optional
        If True, run and time the convolution of `in1` and `in2` with both
        methods and return the fastest. If False (default), predict the fastest
        method using precomputed values.

    Returns
    -------
    method : str
        A string indicating which convolution method is fastest, either
        'direct' or 'fft'
    times : dict, optional
        A dictionary containing the times (in seconds) needed for each method.
        This value is only returned if ``measure=True``.

    See Also
    --------
    convolve
    correlate

    Notes
    -----
    Generally, this method is 99% accurate for 2D signals and 85% accurate
    for 1D signals for randomly chosen input sizes. For precision, use
    ``measure=True`` to find the fastest method by timing the convolution.
    This can be used to avoid the minimal overhead of finding the fastest
    ``method`` later, or to adapt the value of ``method`` to a particular set
    of inputs.

    Experiments were run on an Amazon EC2 r5a.2xlarge machine to test this
    function. These experiments measured the ratio between the time required
    when using ``method='auto'`` and the time required for the fastest method
    (i.e., ``ratio = time_auto / min(time_fft, time_direct)``). In these
    experiments, we found:

    * There is a 95% chance of this ratio being less than 1.5 for 1D signals
      and a 99% chance of being less than 2.5 for 2D signals.
    * The ratio was always less than 2.5/5 for 1D/2D signals respectively.
    * This function is most inaccurate for 1D convolutions that take between 1
      and 10 milliseconds with ``method='direct'``. A good proxy for this
      (at least in our experiments) is ``1e6 <= in1.size * in2.size <= 1e7``.

    The 2D results almost certainly generalize to 3D/4D/etc because the
    implementation is the same (the 1D implementation is different).

    All the numbers above are specific to the EC2 machine. However, we did find
    that this function generalizes fairly decently across hardware. The speed
    tests were of similar quality (and even slightly better) than the same
    tests performed on the machine to tune this function's numbers (a mid-2014
    15-inch MacBook Pro with 16GB RAM and a 2.5GHz Intel i7 processor).

    There are cases when `fftconvolve` supports the inputs but this function
    returns `direct` (e.g., to protect against floating point integer
    precision).

    .. versionadded:: 0.19

    Examples
    --------
    Estimate the fastest method for a given input:

    >>> import numpy as np
    >>> from scipy import signal
    >>> rng = np.random.default_rng()
    >>> img = rng.random((32, 32))
    >>> filter = rng.random((8, 8))
    >>> method = signal.choose_conv_method(img, filter, mode='same')
    >>> method
    'fft'

    This can then be applied to other arrays of the same dtype and shape:

    >>> img2 = rng.random((32, 32))
    >>> filter2 = rng.random((8, 8))
    >>> corr2 = signal.correlate(img2, filter2, mode='same', method=method)
    >>> conv2 = signal.convolve(img2, filter2, mode='same', method=method)

    The output of this function (``method``) works with `correlate` and
    `convolve`.

    """
    xp = array_namespace(in1, in2)

    volume = xp.asarray(in1)
    kernel = xp.asarray(in2)

    if measure:
        times = {}
        for method in ['fft', 'direct']:
            times[method] = _timeit_fast(lambda: convolve(volume, kernel,
                                         mode=mode, method=method))

        chosen_method = 'fft' if times['fft'] < times['direct'] else 'direct'
        return chosen_method, times

    # for integer input,
    # catch when more precision required than float provides (representing an
    # integer as float can lose precision in fftconvolve if larger than 2**52)
    if any([_numeric_arrays([x], kinds='ui', xp=xp) for x in [volume, kernel]]):
        max_value = int(xp.max(xp.abs(volume))) * int(xp.max(xp.abs(kernel)))
        max_value *= int(min(xp_size(volume), xp_size(kernel)))
        if max_value > 2**np.finfo('float').nmant - 1:
            return 'direct'

    if _numeric_arrays([volume, kernel], kinds='b', xp=xp):
        return 'direct'

    if _numeric_arrays([volume, kernel], xp=xp):
        if _fftconv_faster(volume, kernel, mode):
            return 'fft'

    return 'direct'


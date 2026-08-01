
def oaconvolve(in1, in2, mode="full", axes=None):
    """Convolve two N-dimensional arrays using the overlap-add method.

    Convolve `in1` and `in2` using the overlap-add method, with
    the output size determined by the `mode` argument.

    This is generally much faster than `convolve` for large arrays (n > ~500),
    and generally much faster than `fftconvolve` when one array is much
    larger than the other, but can be slower when only a few output values are
    needed or when the arrays are very similar in shape, and can only
    output float arrays (int or object array inputs will be cast to float).

    Parameters
    ----------
    in1 : array_like
        First input.
    in2 : array_like
        Second input. Should have the same number of dimensions as `in1`.
    mode : str {'full', 'valid', 'same'}, optional
        A string indicating the size of the output:

        ``full``
           The output is the full discrete linear convolution
           of the inputs. (Default)
        ``valid``
           The output consists only of those elements that do not
           rely on the zero-padding. In 'valid' mode, either `in1` or `in2`
           must be at least as large as the other in every dimension.
        ``same``
           Output size will be ``N``, the same size as `in1`, centered
           with respect to the 'full' output.
           Boundary effects may be visible.
    axes : int or array_like of ints or None, optional
        Axes over which to compute the convolution.
        The default is over all axes.

    Returns
    -------
    out : array
        An N-dimensional array containing a subset of the discrete linear
        convolution of `in1` with `in2`.

        The output size along each axis depends on ``mode``. For input
        sizes ``N`` and ``M`` along a given axis:

        - ``full`` : ``N + M - 1``
        - ``same`` : ``N`` (same as the size of `in1`)
        - ``valid`` : ``max(N, M) - min(N, M) + 1``

    See Also
    --------
    convolve : Uses the direct convolution or FFT convolution algorithm
               depending on which is faster.
    fftconvolve : An implementation of convolution using FFT.

    Notes
    -----
    .. versionadded:: 1.4.0

    References
    ----------
    .. [1] Wikipedia, "Overlap-add_method".
           https://en.wikipedia.org/wiki/Overlap-add_method
    .. [2] Richard G. Lyons. Understanding Digital Signal Processing,
           Third Edition, 2011. Chapter 13.10.
           ISBN 13: 978-0137-02741-5

    Examples
    --------
    Convolve a 100,000 sample signal with a 512-sample filter.

    >>> import numpy as np
    >>> from scipy import signal
    >>> rng = np.random.default_rng()
    >>> sig = rng.standard_normal(100000)
    >>> filt = signal.firwin(512, 0.01)
    >>> fsig = signal.oaconvolve(sig, filt)

    >>> import matplotlib.pyplot as plt
    >>> fig, (ax_orig, ax_mag) = plt.subplots(2, 1)
    >>> ax_orig.plot(sig)
    >>> ax_orig.set_title('White noise')
    >>> ax_mag.plot(fsig)
    >>> ax_mag.set_title('Filtered noise')
    >>> fig.tight_layout()
    >>> fig.show()

    """
    xp = array_namespace(in1, in2)

    in1 = xp.asarray(in1)
    in2 = xp.asarray(in2)

    if in1.ndim == in2.ndim == 0:  # scalar inputs
        return in1 * in2
    elif in1.ndim != in2.ndim:
        raise ValueError("in1 and in2 should have the same dimensionality")
    elif in1.size == 0 or in2.size == 0:  # empty arrays
        return xp.asarray([])
    elif in1.shape == in2.shape:  # Equivalent to fftconvolve
        return fftconvolve(in1, in2, mode=mode, axes=axes)

    in1, in2, axes = _init_freq_conv_axes(in1, in2, mode, axes,
                                          sorted_axes=True)

    s1 = in1.shape
    s2 = in2.shape

    if not axes:
        ret = in1 * in2
        return _apply_conv_mode(ret, s1, s2, mode, axes, xp)

    # Calculate this now since in1 is changed later
    shape_final = [None if i not in axes else
                   s1[i] + s2[i] - 1 for i in range(in1.ndim)]

    # Calculate the block sizes for the output, steps, first and second inputs.
    # It is simpler to calculate them all together than doing them in separate
    # loops due to all the special cases that need to be handled.
    optimal_sizes = ((-1, -1, s1[i], s2[i]) if i not in axes else
                     _calc_oa_lens(s1[i], s2[i]) for i in range(in1.ndim))
    block_size, overlaps, \
        in1_step, in2_step = zip(*optimal_sizes)

    # Fall back to fftconvolve if there is only one block in every dimension.
    if in1_step == s1 and in2_step == s2:
        return fftconvolve(in1, in2, mode=mode, axes=axes)

    # Figure out the number of steps and padding.
    # This would get too complicated in a list comprehension.
    nsteps1 = []
    nsteps2 = []
    pad_size1 = []
    pad_size2 = []
    for i in range(in1.ndim):
        if i not in axes:
            pad_size1 += [(0, 0)]
            pad_size2 += [(0, 0)]
            continue

        if s1[i] > in1_step[i]:
            curnstep1 = math.ceil((s1[i]+1)/in1_step[i])
            if (block_size[i] - overlaps[i])*curnstep1 < shape_final[i]:
                curnstep1 += 1

            curpad1 = curnstep1*in1_step[i] - s1[i]
        else:
            curnstep1 = 1
            curpad1 = 0

        if s2[i] > in2_step[i]:
            curnstep2 = math.ceil((s2[i]+1)/in2_step[i])
            if (block_size[i] - overlaps[i])*curnstep2 < shape_final[i]:
                curnstep2 += 1

            curpad2 = curnstep2*in2_step[i] - s2[i]
        else:
            curnstep2 = 1
            curpad2 = 0

        nsteps1 += [curnstep1]
        nsteps2 += [curnstep2]
        pad_size1 += [(0, curpad1)]
        pad_size2 += [(0, curpad2)]

    # Pad the array to a size that can be reshaped to the desired shape
    # if necessary.
    if not all(curpad == (0, 0) for curpad in pad_size1):
        in1 = xpx.pad(in1, pad_size1, mode='constant', constant_values=0, xp=xp)

    if not all(curpad == (0, 0) for curpad in pad_size2):
         in2 = xpx.pad(in2, pad_size2, mode='constant', constant_values=0, xp=xp)

    # Reshape the overlap-add parts to input block sizes.
    split_axes = [iax+i for i, iax in enumerate(axes)]
    fft_axes = [iax+1 for iax in split_axes]

    # We need to put each new dimension before the corresponding dimension
    # being reshaped in order to get the data in the right layout at the end.
    reshape_size1 = list(in1_step)
    reshape_size2 = list(in2_step)
    for i, iax in enumerate(split_axes):
        reshape_size1.insert(iax, nsteps1[i])
        reshape_size2.insert(iax, nsteps2[i])

    in1 = xp.reshape(in1, tuple(reshape_size1))
    in2 = xp.reshape(in2, tuple(reshape_size2))

    # Do the convolution.
    fft_shape = [block_size[i] for i in axes]
    ret = _freq_domain_conv(xp, in1, in2, fft_axes, fft_shape, calc_fast_len=False)

    # Do the overlap-add.
    for ax, ax_fft, ax_split in zip(axes, fft_axes, split_axes):
        overlap = overlaps[ax]
        if overlap is None:
            continue

        ret, overpart = _split(ret, [-overlap], ax_fft, xp=xp)
        overpart = _split(overpart, [-1], ax_split, xp=xp)[0]

        overlap_slice = [slice(None)] * ret.ndim
        overlap_slice[ax_fft] = slice(0, overlap)
        overlap_slice[ax_split] = slice(1, None)
        ret = xpx.at(ret)[tuple(overlap_slice)].add(overpart)

    # Reshape back to the correct dimensionality.
    shape_ret = [ret.shape[i] if i not in fft_axes else
                 ret.shape[i]*ret.shape[i-1]
                 for i in range(ret.ndim) if i not in split_axes]
    ret = xp.reshape(ret, tuple(shape_ret))

    # Slice to the correct size.
    slice_final = tuple([slice(islice) for islice in shape_final])
    ret = ret[slice_final]

    return _apply_conv_mode(ret, s1, s2, mode, axes, xp)


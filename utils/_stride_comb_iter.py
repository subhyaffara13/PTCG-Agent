import itertools

def _stride_comb_iter(x):
    """
    Generate cartesian product of strides for all axes
    """

    if not isinstance(x, np.ndarray):
        yield x, "nop"
        return

    stride_set = [(1,)] * x.ndim
    stride_set[-1] = (1, 3, -4)
    if x.ndim > 1:
        stride_set[-2] = (1, 3, -4)
    if x.ndim > 2:
        stride_set[-3] = (1, -4)

    for repeats in itertools.product(*tuple(stride_set)):
        new_shape = [abs(a * b) for a, b in zip(x.shape, repeats)]
        slices = tuple(slice(None, None, repeat) for repeat in repeats)

        # new array with different strides, but same data
        xi = np.empty(new_shape, dtype=x.dtype)
        xi.view(np.uint32).fill(0xdeadbeef)
        xi = xi[slices]
        xi[...] = x
        xi = xi.view(x.__class__)
        assert_(np.all(xi == x))
        yield xi, "stride_" + "_".join(f"{j:+}" for j in repeats)

        # generate also zero strides if possible
        if x.ndim >= 1 and x.shape[-1] == 1:
            s = list(x.strides)
            s[-1] = 0
            xi = np.lib.stride_tricks.as_strided(x, strides=s)
            yield xi, "stride_xxx_0"
        if x.ndim >= 2 and x.shape[-2] == 1:
            s = list(x.strides)
            s[-2] = 0
            xi = np.lib.stride_tricks.as_strided(x, strides=s)
            yield xi, "stride_xxx_0_x"
        if x.ndim >= 2 and x.shape[:-2] == (1, 1):
            s = list(x.strides)
            s[-1] = 0
            s[-2] = 0
            xi = np.lib.stride_tricks.as_strided(x, strides=s)
            yield xi, "stride_xxx_0_0"


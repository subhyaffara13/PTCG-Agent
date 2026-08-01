
def _elements_and_indices_with_max_real(a, *, axis=-1, xp):
    # This is an array-API compatible `max` function that works something
    # like `np.max` for complex input. The important part is that it finds
    # the element with maximum real part. When there are multiple complex values
    # with this real part, it doesn't matter which we choose.
    # We could use `argmax` on real component, but array API doesn't yet have
    # `take_along_axis`, and even if it did, we would have problems with axis tuples.
    # Feel free to rewrite! It's ugly, but it's not the purpose of the PR, and
    # it gets the job done.

    if xp.isdtype(a.dtype, "complex floating"):
        # select all elements with max real part.
        real_a = xp.real(a)
        max_ = xp.max(real_a, axis=axis, keepdims=True)
        mask = real_a == max_

        # Of those, choose one arbitrarily. This is a reasonably
        # simple, array-API compatible way of doing so that doesn't
        # have a problem with `axis` being a tuple or None.
        i = xp.reshape(xp.arange(xp_size(a), device=xp_device(a)), a.shape)
        i = xpx.at(i, ~mask).set(-1)
        max_i = xp.max(i, axis=axis, keepdims=True)
        mask = i == max_i
        a = xp.where(mask, a, 0.)
        max_ = xp.sum(a, axis=axis, dtype=a.dtype, keepdims=True)
    else:
        max_ = xp.max(a, axis=axis, keepdims=True)
        mask = a == max_

    return max_, mask


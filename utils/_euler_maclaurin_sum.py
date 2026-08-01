
def _euler_maclaurin_sum(fj, work, xp):
    # Perform the Euler-Maclaurin Sum, [1] Section 4

    # The error estimate needs to know the magnitude of the last term
    # omitted from the Euler-Maclaurin sum. This is a bit involved because
    # it may have been computed at a previous level. I sure hope it's worth
    # all the trouble.
    xr0, fr0, wr0 = work.xr0, work.fr0, work.wr0
    xl0, fl0, wl0 = work.xl0, work.fl0, work.wl0

    # It is much more convenient to work with the transposes of our work
    # variables here.
    xj, fj, wj = work.xj.T, fj.T, work.wj.T
    n_x, n_active = xj.shape  # number of abscissae, number of active elements

    # We'll work with the left and right sides separately
    xr, xl = xp_copy(xp.reshape(xj, (2, n_x // 2, n_active)))  # this gets modified
    fr, fl = xp.reshape(fj, (2, n_x // 2, n_active))
    wr, wl = xp.reshape(wj, (2, n_x // 2, n_active))

    invalid_r = ~xp.isfinite(fr) | (wr == 0)
    invalid_l = ~xp.isfinite(fl) | (wl == 0)

    # integer index of the maximum abscissa at this level
    xr[invalid_r] = -xp.inf
    ir = xp.argmax(xp.real(xr), axis=0, keepdims=True)
    # abscissa, function value, and weight at this index
    ### Not Array API Compatible... yet ###
    xr_max = xp.take_along_axis(xr, ir, axis=0)[0]
    fr_max = xp.take_along_axis(fr, ir, axis=0)[0]
    wr_max = xp.take_along_axis(wr, ir, axis=0)[0]
    # boolean indices at which maximum abscissa at this level exceeds
    # the incumbent maximum abscissa (from all previous levels)
    # note: abscissa may have complex dtype, but will have zero imaginary part
    j = xp.real(xr_max) > xp.real(xr0)
    # Update record of the incumbent abscissa, function value, and weight
    xr0[j] = xr_max[j]
    fr0[j] = fr_max[j]
    wr0[j] = wr_max[j]

    # integer index of the minimum abscissa at this level
    xl[invalid_l] = xp.inf
    il = xp.argmin(xp.real(xl), axis=0, keepdims=True)
    # abscissa, function value, and weight at this index
    xl_min = xp.take_along_axis(xl, il, axis=0)[0]
    fl_min = xp.take_along_axis(fl, il, axis=0)[0]
    wl_min = xp.take_along_axis(wl, il, axis=0)[0]
    # boolean indices at which minimum abscissa at this level is less than
    # the incumbent minimum abscissa (from all previous levels)
    # note: abscissa may have complex dtype, but will have zero imaginary part
    j = xp.real(xl_min) < xp.real(xl0)
    # Update record of the incumbent abscissa, function value, and weight
    xl0[j] = xl_min[j]
    fl0[j] = fl_min[j]
    wl0[j] = wl_min[j]
    fj = fj.T

    # Compute the error estimate `d4` - the magnitude of the leftmost or
    # rightmost term, whichever is greater.
    flwl0 = fl0 + xp.log(wl0) if work.log else fl0 * wl0  # leftmost term
    frwr0 = fr0 + xp.log(wr0) if work.log else fr0 * wr0  # rightmost term
    magnitude = xp.real if work.log else xp.abs
    work.d4 = xp.maximum(magnitude(flwl0), magnitude(frwr0))

    # There are two approaches to dealing with function values that are
    # numerically infinite due to approaching a singularity - zero them, or
    # replace them with the function value at the nearest non-infinite point.
    # [3] pg. 22 suggests the latter, so let's do that given that we have the
    # information.
    fr0b = xp.broadcast_to(fr0[xp.newaxis, :], fr.shape)
    fl0b = xp.broadcast_to(fl0[xp.newaxis, :], fl.shape)
    fr[invalid_r] = fr0b[invalid_r]
    fl[invalid_l] = fl0b[invalid_l]

    # When wj is zero, log emits a warning
    # with np.errstate(divide='ignore'):
    fjwj = fj + xp.log(work.wj) if work.log else fj * work.wj

    # update integral estimate
    Sn = (special.logsumexp(fjwj + xp.log(work.h), axis=-1) if work.log
          else xp.sum(fjwj, axis=-1) * work.h)

    work.xr0, work.fr0, work.wr0 = xr0, fr0, wr0
    work.xl0, work.fl0, work.wl0 = xl0, fl0, wl0

    return fjwj, Sn


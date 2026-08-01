
def _integral_bound(f, a, b, step, args, constants, xp):
    # Estimate the sum with integral approximation
    dtype, log, _, _, rtol, atol, maxterms = constants
    log2 = xp.asarray(math.log(2), dtype=dtype)

    # Get a lower bound on the sum and compute effective absolute tolerance
    lb = tanhsinh(f, a, b, args=args, atol=atol, rtol=rtol, log=log)
    tol = xp.broadcast_to(xp.asarray(atol), lb.integral.shape)
    if log:
        tol = special.logsumexp(xp.stack((tol, rtol + lb.integral)), axis=0)
    else:
        tol = tol + rtol*lb.integral
    i_skip = lb.status == -3  # avoid unnecessary f_evals if integral is divergent
    tol[i_skip] = xp.nan
    status = lb.status

    # As in `_direct`, we'll need a temporary new axis for points
    # at which to evaluate the function. Append axis at the end for
    # consistency with other elementwise algorithms.
    a2 = a[..., xp.newaxis]
    step2 = step[..., xp.newaxis]
    args2 = [arg[..., xp.newaxis] for arg in args]

    # Find the location of a term that is less than the tolerance (if possible)
    log2maxterms = math.floor(math.log2(maxterms)) if maxterms else 0
    n_steps = xp.concat((2**xp.arange(0, log2maxterms), xp.asarray([maxterms])))
    n_steps = xp.astype(n_steps, dtype)
    nfev = len(n_steps) * 2
    ks = a2 + n_steps * step2
    fks = f(ks, *args2)
    fksp1 = f(ks + step2, *args2)  # check that the function is decreasing
    fk_insufficient = (fks > tol[:, xp.newaxis]) | (fksp1 > fks)
    n_fk_insufficient = xp.sum(fk_insufficient, axis=-1)
    nt = xp.minimum(n_fk_insufficient, n_steps.shape[-1]-1)
    n_steps = n_steps[nt]

    # If `maxterms` is insufficient (i.e. either the magnitude of the last term of the
    # partial sum exceeds the tolerance or the function is not decreasing), finish the
    # calculation, but report nonzero status. (Improvement: separate the status codes
    # for these two cases.)
    i_fk_insufficient = (n_fk_insufficient == nfev//2)

    # Directly evaluate the sum up to this term
    k = a + n_steps * step
    left, left_error, left_nfev = _direct(f, a, k, step, args,
                                          constants, xp, inclusive=False)
    left_is_pos_inf = xp.isinf(left) & (left > 0)
    i_skip |= left_is_pos_inf  # if sum is infinite, no sense in continuing
    status[left_is_pos_inf] = -3
    k[i_skip] = xp.nan

    # Use integration to estimate the remaining sum
    # Possible optimization for future work: if there were no terms less than
    # the tolerance, there is no need to compute the integral to better accuracy.
    # Something like:
    # atol = xp.maximum(atol, xp.minimum(fk/2 - fb/2))
    # rtol = xp.maximum(rtol, xp.minimum((fk/2 - fb/2)/left))
    # where `fk`/`fb` are currently calculated below.
    right = tanhsinh(f, k, b, args=args, atol=atol, rtol=rtol, log=log)

    # Calculate the full estimate and error from the pieces
    fk = fks[xp.arange(len(fks)), nt]

    # fb = f(b, *args), but some functions return NaN at infinity.
    # instead of 0 like they must (for the sum to be convergent).
    fb = xp.full_like(fk, -xp.inf) if log else xp.zeros_like(fk)
    i = xp.isfinite(b)
    if xp.any(i):  # better not call `f` with empty arrays
        fb[i] = f(b[i], *[arg[i] for arg in args])
    nfev = nfev + xp.asarray(i, dtype=left_nfev.dtype)

    if log:
        log_step = xp.log(step)
        S_terms = (left, right.integral - log_step, fk - log2, fb - log2)
        S = special.logsumexp(xp.stack(S_terms), axis=0)
        E_terms = (left_error, right.error - log_step, fk-log2, fb-log2+xp.pi*1j)
        E = xp.real(special.logsumexp(xp.stack(E_terms), axis=0))
    else:
        S = left + right.integral/step + fk/2 + fb/2
        E = left_error + right.error/step + fk/2 - fb/2
    status[~i_skip] = right.status[~i_skip]

    status[(status == 0) & i_fk_insufficient] = -4
    return S, E, status, left_nfev + right.nfev + nfev + lb.nfev


import math


def _direct(f, a, b, step, args, constants, xp, inclusive=True):
    # Directly evaluate the sum.

    # When used in the context of distributions, `args` would contain the
    # distribution parameters. We have broadcasted for simplicity, but we could
    # reduce function evaluations when distribution parameters are the same but
    # sum limits differ. Roughly:
    # - compute the function at all points between min(a) and max(b),
    # - compute the cumulative sum,
    # - take the difference between elements of the cumulative sum
    #   corresponding with b and a.
    # This is left to future enhancement

    dtype, log, eps, zero, _, _, _ = constants

    # To allow computation in a single vectorized call, find the maximum number
    # of points (over all slices) at which the function needs to be evaluated.
    # Note: if `inclusive` is `True`, then we want `1` more term in the sum.
    # I didn't think it was great style to use `True` as `1` in Python, so I
    # explicitly converted it to an `int` before using it.
    inclusive_adjustment = int(inclusive)
    steps = xp.round((b - a) / step) + inclusive_adjustment
    # Equivalently, steps = xp.round((b - a) / step) + inclusive
    max_steps = int(xp.max(steps))

    # In each slice, the function will be evaluated at the same number of points,
    # but excessive points (those beyond the right sum limit `b`) are replaced
    # with NaN to (potentially) reduce the time of these unnecessary calculations.
    # Use a new last axis for these calculations for consistency with other
    # elementwise algorithms.
    a2, b2, step2 = a[:, xp.newaxis], b[:, xp.newaxis], step[:, xp.newaxis]
    args2 = [arg[:, xp.newaxis] for arg in args]
    ks = a2 + xp.arange(max_steps, dtype=dtype) * step2
    i_nan = ks >= (b2 + inclusive_adjustment*step2/2)
    ks[i_nan] = xp.nan
    fs = f(ks, *args2)

    # The function evaluated at NaN is NaN, and NaNs are zeroed in the sum.
    # In some cases it may be faster to loop over slices than to vectorize
    # like this. This is an optimization that can be added later.
    fs[i_nan] = zero
    nfev = max_steps - i_nan.sum(axis=-1)
    S = special.logsumexp(fs, axis=-1) if log else xp.sum(fs, axis=-1)
    # Rough, non-conservative error estimate. See gh-19667 for improvement ideas.
    E = xp.real(S) + math.log(eps) if log else eps * abs(S)
    return S, E, nfev


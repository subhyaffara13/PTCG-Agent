
def _recover_from_bracket_error(solver, fun, bracket, args, **options):
    # `bracket` was originally written without checking whether the resulting
    # bracket is valid. `brent` and `golden` built on top of it without
    # checking the returned bracket for validity, and their output can be
    # incorrect without warning/error if the original bracket is invalid.
    # gh-14858 noticed the problem, and the following is the desired
    # behavior:
    # - `scipy.optimize.bracket`, `scipy.optimize.brent`, and
    #   `scipy.optimize.golden` should raise an error if the bracket is
    #   invalid, as opposed to silently returning garbage
    # - `scipy.optimize.minimize_scalar` should return with `success=False`
    #   and other information
    # The changes that would be required to achieve this the traditional
    # way (`return`ing all the required information from bracket all the way
    # up to `minimizer_scalar`) are extensive and invasive. (See a6aa40d.)
    # We can achieve the same thing by raising the error in `bracket`, but
    # storing the information needed by `minimize_scalar` in the error object,
    # and intercepting it here.
    try:
        res = solver(fun, bracket, args, **options)
    except BracketError as e:
        msg = str(e)
        xa, xb, xc, fa, fb, fc, funcalls = e.data
        xs, fs = [xa, xb, xc], [fa, fb, fc]
        if np.any(np.isnan([xs, fs])):
            x, fun = np.nan, np.nan
        else:
            imin = np.argmin(fs)
            x, fun = xs[imin], fs[imin]
        return OptimizeResult(fun=fun, nfev=funcalls, x=x,
                              nit=0, success=False, message=msg)
    return res



def _iv(A, k, ncv, tol, which, v0, maxiter,
        return_singular, solver, rng):

    # input validation/standardization for `solver`
    # out of order because it's needed for other parameters
    solver = str(solver).lower()
    solvers = {"arpack", "lobpcg", "propack"}
    if solver not in solvers:
        raise ValueError(f"solver must be one of {solvers}.")

    # input validation/standardization for `A`
    A = aslinearoperator(A)  # this takes care of some input validation
    if not np.issubdtype(A.dtype, np.number):
        message = "`A` must be of numeric data type."
        raise ValueError(message)
    if math.prod(A.shape) == 0:
        message = "`A` must not be empty."
        raise ValueError(message)
    if A.ndim != 2:
        raise ValueError("Only 2-D input is supported for `A` (a single matrix)")

    # input validation/standardization for `k`
    kmax = min(A.shape) if solver == 'propack' else min(A.shape) - 1
    if int(k) != k or not (0 < k <= kmax):
        message = "`k` must be an integer satisfying `0 < k < min(A.shape)`."
        raise ValueError(message)
    k = int(k)

    # input validation/standardization for `ncv`
    if solver == "arpack" and ncv is not None:
        if int(ncv) != ncv or not (k < ncv < min(A.shape)):
            message = ("`ncv` must be an integer satisfying "
                       "`k < ncv < min(A.shape)`.")
            raise ValueError(message)
        ncv = int(ncv)

    # input validation/standardization for `tol`
    if tol < 0 or not np.isfinite(tol):
        message = "`tol` must be a non-negative floating point value."
        raise ValueError(message)
    tol = float(tol)

    # input validation/standardization for `which`
    which = str(which).upper()
    whichs = {'LM', 'SM'}
    if which not in whichs:
        raise ValueError(f"`which` must be in {whichs}.")

    # input validation/standardization for `v0`
    if v0 is not None:
        v0 = np.atleast_1d(v0)
        if not (np.issubdtype(v0.dtype, np.complexfloating)
                or np.issubdtype(v0.dtype, np.floating)):
            message = ("`v0` must be of floating or complex floating "
                       "data type.")
            raise ValueError(message)

        shape = (A.shape[0],) if solver == 'propack' else (min(A.shape),)
        if v0.shape != shape:
            message = f"`v0` must have shape {shape}."
            raise ValueError(message)

    # input validation/standardization for `maxiter`
    if maxiter is not None and (int(maxiter) != maxiter or maxiter <= 0):
        message = "`maxiter` must be a positive integer."
        raise ValueError(message)
    maxiter = int(maxiter) if maxiter is not None else maxiter

    # input validation/standardization for `return_singular_vectors`
    # not going to be flexible with this; too complicated for little gain
    rs_options = {True, False, "vh", "u"}
    if return_singular not in rs_options:
        raise ValueError(f"`return_singular_vectors` must be in {rs_options}.")

    rng = check_random_state(rng)

    return (A, k, ncv, tol, which, v0, maxiter,
            return_singular, solver, rng)


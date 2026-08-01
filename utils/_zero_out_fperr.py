
def _zero_out_fperr(arg, tol: float | np.ndarray):
    # #18044 reference this behavior to fix rolling skew/kurt issue
    if isinstance(arg, np.ndarray):
        return np.where(np.abs(arg) < tol, 0, arg)
    else:
        return arg.dtype.type(0) if np.abs(arg) < tol else arg


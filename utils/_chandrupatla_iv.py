
def _chandrupatla_iv(func, args, kwargs, xatol, xrtol,
                     fatol, frtol, maxiter, callback):
    # Input validation for `_chandrupatla`

    if not callable(func):
        raise ValueError('`func` must be callable.')

    if not np.iterable(args):
        args = (args,)

    # tolerances are floats, not arrays; OK to use NumPy
    tols = np.asarray([xatol if xatol is not None else 1,
                       xrtol if xrtol is not None else 1,
                       fatol if fatol is not None else 1,
                       frtol if frtol is not None else 1])
    if (not np.issubdtype(tols.dtype, np.number) or np.any(tols < 0)
            or np.any(np.isnan(tols)) or tols.shape != (4,)):
        raise ValueError('Tolerances must be non-negative scalars.')

    if maxiter is not None:
        maxiter_int = int(maxiter)
        if maxiter != maxiter_int or maxiter < 0:
            raise ValueError('`maxiter` must be a non-negative integer.')

    if callback is not None and not callable(callback):
        raise ValueError('`callback` must be callable.')

    return func, args, kwargs, xatol, xrtol, fatol, frtol, maxiter, callback


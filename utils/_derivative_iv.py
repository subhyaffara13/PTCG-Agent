
def _derivative_iv(f, x, args, kwargs, tolerances, maxiter, order, initial_step,
                   step_factor, step_direction, preserve_shape, callback):
    # Input validation for `derivative`
    xp = array_namespace(x)

    if not callable(f):
        raise ValueError('`f` must be callable.')

    if not np.iterable(args):
        args = (args,)

    tolerances = {} if tolerances is None else tolerances
    atol = tolerances.get('atol', None)
    rtol = tolerances.get('rtol', None)

    # tolerances are floats, not arrays; OK to use NumPy
    message = 'Tolerances and step parameters must be non-negative scalars.'
    tols = np.asarray([atol if atol is not None else 1,
                       rtol if rtol is not None else 1,
                       step_factor])
    if (not np.issubdtype(tols.dtype, np.number) or np.any(tols < 0)
            or np.any(np.isnan(tols)) or tols.shape != (3,)):
        raise ValueError(message)
    step_factor = float(tols[2])

    maxiter_int = int(maxiter)
    if maxiter != maxiter_int or maxiter <= 0:
        raise ValueError('`maxiter` must be a positive integer.')

    order_int = int(order)
    if order_int != order or order <= 0:
        raise ValueError('`order` must be a positive integer.')

    step_direction = xp.asarray(step_direction)
    initial_step = xp.asarray(initial_step)
    temp = xp.broadcast_arrays(x, step_direction, initial_step)
    x, step_direction, initial_step = temp

    message = '`preserve_shape` must be True or False.'
    if preserve_shape not in {True, False}:
        raise ValueError(message)

    if callback is not None and not callable(callback):
        raise ValueError('`callback` must be callable.')

    return (f, x, args, kwargs, atol, rtol, maxiter_int, order_int, initial_step,
            step_factor, step_direction, preserve_shape, callback)


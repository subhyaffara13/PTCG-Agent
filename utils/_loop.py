import math


def _loop(work, callback, shape, maxiter, func, args, dtype, pre_func_eval,
          post_func_eval, check_termination, post_termination_check,
          customize_result, res_work_pairs, xp, preserve_shape=False):
    """Main loop of a vectorized scalar optimization algorithm

    Parameters
    ----------
    work : _RichResult
        All variables that need to be retained between iterations. Must
        contain attributes `nit`, `nfev`, and `success`. All arrays are
        subject to being "compressed" if `preserve_shape is False`; nest
        arrays that should not be compressed inside another object (e.g.
        `dict` or `_RichResult`).
    callback : callable
        User-specified callback function
    shape : tuple of ints
        The shape of all output arrays
    maxiter :
        Maximum number of iterations of the algorithm
    func : callable
        The user-specified callable that is being optimized or solved
    args : tuple
        Additional positional arguments to be passed to `func`.
    dtype : NumPy dtype
        The common dtype of all abscissae and function values
    pre_func_eval : callable
        A function that accepts `work` and returns `x`, the active elements
        of `x` at which `func` will be evaluated. May modify attributes
        of `work` with any algorithmic steps that need to happen
         at the beginning of an iteration, before `func` is evaluated,
    post_func_eval : callable
        A function that accepts `x`, `func(x)`, and `work`. May modify
        attributes of `work` with any algorithmic steps that need to happen
         in the middle of an iteration, after `func` is evaluated but before
         the termination check.
    check_termination : callable
        A function that accepts `work` and returns `stop`, a boolean array
        indicating which of the active elements have met a termination
        condition.
    post_termination_check : callable
        A function that accepts `work`. May modify `work` with any algorithmic
        steps that need to happen after the termination check and before the
        end of the iteration.
    customize_result : callable
        A function that accepts `res` and `shape` and returns `shape`. May
        modify `res` (in-place) according to preferences (e.g. rearrange
        elements between attributes) and modify `shape` if needed.
    res_work_pairs : list of (str, str)
        Identifies correspondence between attributes of `res` and attributes
        of `work`; i.e., attributes of active elements of `work` will be
        copied to the appropriate indices of `res` when appropriate. The order
        determines the order in which _RichResult attributes will be
        pretty-printed.
    preserve_shape : bool, default: False
        Whether to compress the attributes of `work` (to avoid unnecessary
        computation on elements that have already converged).

    Returns
    -------
    res : _RichResult
        The final result object

    Notes
    -----
    Besides providing structure, this framework provides several important
    services for a vectorized optimization algorithm.

    - It handles common tasks involving iteration count, function evaluation
      count, a user-specified callback, and associated termination conditions.
    - It compresses the attributes of `work` to eliminate unnecessary
      computation on elements that have already converged.

    """
    if xp is None:
        raise NotImplementedError("Must provide xp.")

    cb_terminate = False

    # Initialize the result object and active element index array
    n_elements = math.prod(shape)
    active = xp.arange(n_elements)  # in-progress element indices
    res_dict = {i: xp.zeros(n_elements, dtype=dtype) for i, j in res_work_pairs}
    res_dict['success'] = xp.zeros(n_elements, dtype=xp.bool)
    res_dict['status'] = xp.full(n_elements, xp.asarray(_EINPROGRESS), dtype=xp.int32)
    res_dict['nit'] = xp.zeros(n_elements, dtype=xp.int32)
    res_dict['nfev'] = xp.zeros(n_elements, dtype=xp.int32)
    res = _RichResult(res_dict)
    work.args = args

    active = _check_termination(work, res, res_work_pairs, active,
                                check_termination, preserve_shape, xp)

    if callback is not None:
        temp = _prepare_result(work, res, res_work_pairs, active, shape,
                               customize_result, preserve_shape, xp)
        if _call_callback_maybe_halt(callback, temp):
            cb_terminate = True

    while work.nit < maxiter and xp_size(active) and not cb_terminate and n_elements:
        x = pre_func_eval(work)

        if work.args and work.args[0].ndim != x.ndim:
            # `x` always starts as 1D. If the SciPy function that uses
            # _loop added dimensions to `x`, we need to
            # add them to the elements of `args`.
            args = []
            for arg in work.args:
                n_new_dims = x.ndim - arg.ndim
                new_shape = arg.shape + (1,)*n_new_dims
                args.append(xp.reshape(arg, new_shape))
            work.args = args

        x_shape = x.shape
        if preserve_shape:
            x = xp.reshape(x, (shape + (-1,)))
        f = func(x, *work.args)
        f = xp.asarray(f, dtype=dtype)
        if preserve_shape:
            x = xp.reshape(x, x_shape)
            f = xp.reshape(f, x_shape)
        work.nfev += 1 if x.ndim == 1 else x.shape[-1]

        post_func_eval(x, f, work)

        work.nit += 1
        active = _check_termination(work, res, res_work_pairs, active,
                                    check_termination, preserve_shape, xp)

        if callback is not None:
            temp = _prepare_result(work, res, res_work_pairs, active, shape,
                                   customize_result, preserve_shape, xp)
            if _call_callback_maybe_halt(callback, temp):
                cb_terminate = True
                break
        if xp_size(active) == 0:
            break

        post_termination_check(work)

    work.status = xpx.at(work.status)[:].set(_ECALLBACK if cb_terminate else _ECONVERR)
    return _prepare_result(work, res, res_work_pairs, active, shape,
                           customize_result, preserve_shape, xp)


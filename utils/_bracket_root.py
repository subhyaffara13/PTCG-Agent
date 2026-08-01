
def _bracket_root(func, xl0, xr0=None, *, xmin=None, xmax=None, factor=None,
                  args=(), kwargs=None, maxiter=1000):
    """Bracket the root of a monotonic scalar function of one variable

    This function works elementwise when `xl0`, `xr0`, `xmin`, `xmax`, `factor`, and
    the elements of `args` are broadcastable arrays.

    Parameters
    ----------
    func : callable
        The function for which the root is to be bracketed.
        The signature must be::

            func(x: ndarray, *args) -> ndarray

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with `x`. ``func`` must be an elementwise function: each element
        ``func(x)[i]`` must equal ``func(x[i])`` for all indices ``i``.
    xl0, xr0: float array_like
        Starting guess of bracket, which need not contain a root. If `xr0` is
        not provided, ``xr0 = xl0 + 1``. Must be broadcastable with one another.
    xmin, xmax : float array_like, optional
        Minimum and maximum allowable endpoints of the bracket, inclusive. Must
        be broadcastable with `xl0` and `xr0`.
    factor : float array_like, default: 2
        The factor used to grow the bracket. See notes for details.
    args : tuple, optional
        Additional positional arguments to be passed to `func`.  Must be arrays
        broadcastable with `xl0`, `xr0`, `xmin`, and `xmax`. If the callable to be
        bracketed requires arguments that are not broadcastable with these
        arrays, wrap that callable with `func` such that `func` accepts
        only `x` and broadcastable arrays.
    kwargs : dict of str:array_like, optional
        Additional keyword arguments to be passed to `func`. See `args`.
    maxiter : int, optional
        The maximum number of iterations of the algorithm to perform.

    Returns
    -------
    res : _RichResult
        An instance of `scipy._lib._util._RichResult` with the following
        attributes. The descriptions are written as though the values will be
        scalars; however, if `func` returns an array, the outputs will be
        arrays of the same shape.

        xl, xr : float
            The lower and upper ends of the bracket, if the algorithm
            terminated successfully.
        fl, fr : float
            The function value at the lower and upper ends of the bracket.
        nfev : int
            The number of function evaluations required to find the bracket.
            This is distinct from the number of times `func` is *called*
            because the function may evaluated at multiple points in a single
            call.
        nit : int
            The number of iterations of the algorithm that were performed.
        status : int
            An integer representing the exit status of the algorithm.

            - ``0`` : The algorithm produced a valid bracket.
            - ``-1`` : The bracket expanded to the allowable limits without finding a bracket.
            - ``-2`` : The maximum number of iterations was reached.
            - ``-3`` : A non-finite value was encountered.
            - ``-4`` : Iteration was terminated by `callback`.
            - ``-5``: The initial bracket does not satisfy `xmin <= xl0 < xr0 < xmax`.
            - ``1`` : The algorithm is proceeding normally (in `callback` only).
            - ``2`` : A bracket was found in the opposite search direction (in `callback` only).

        success : bool
            ``True`` when the algorithm terminated successfully (status ``0``).

    Notes
    -----
    This function generalizes an algorithm found in pieces throughout
    `scipy.stats`. The strategy is to iteratively grow the bracket ``(l, r)``
     until ``func(l) < 0 < func(r)``. The bracket grows to the left as follows.

    - If `xmin` is not provided, the distance between `xl0` and `l` is iteratively
      increased by `factor`.
    - If `xmin` is provided, the distance between `xmin` and `l` is iteratively
      decreased by `factor`. Note that this also *increases* the bracket size.

    Growth of the bracket to the right is analogous.

    Growth of the bracket in one direction stops when the endpoint is no longer
    finite, the function value at the endpoint is no longer finite, or the
    endpoint reaches its limiting value (`xmin` or `xmax`). Iteration terminates
    when the bracket stops growing in both directions, the bracket surrounds
    the root, or a root is found (accidentally).

    If two brackets are found - that is, a bracket is found on both sides in
    the same iteration, the smaller of the two is returned.
    If roots of the function are found, both `l` and `r` are set to the
    leftmost root.

    """  # noqa: E501
    # Todo:
    # - find bracket with sign change in specified direction
    # - Add tolerance
    # - allow factor < 1?

    callback = None  # works; I just don't want to test it
    temp = _bracket_root_iv(func, xl0, xr0, xmin, xmax, factor, args, kwargs, maxiter)
    func, xl0, xr0, xmin, xmax, factor, args, kwargs, maxiter, xp = temp

    xs = (xl0, xr0)
    temp = eim._initialize(func, xs, args, kwargs=kwargs)
    func, xs, fs, args, shape, dtype, xp = temp  # line split for PEP8
    xl0, xr0 = xs
    xmin = xp_ravel(xp.astype(xp.broadcast_to(xmin, shape), dtype, copy=False), xp=xp)
    xmax = xp_ravel(xp.astype(xp.broadcast_to(xmax, shape), dtype, copy=False), xp=xp)
    invalid_bracket = ~((xmin <= xl0) & (xl0 < xr0) & (xr0 <= xmax))

    # The approach is to treat the left and right searches as though they were
    # (almost) totally independent one-sided bracket searches. (The interaction
    # is considered when checking for termination and preparing the result
    # object.)
    # `x` is the "moving" end of the bracket
    x = xp.concat(xs)
    f = xp.concat(fs)
    invalid_bracket = xp.concat((invalid_bracket, invalid_bracket))
    n = x.shape[0] // 2

    # `x_last` is the previous location of the moving end of the bracket. If
    # the signs of `f` and `f_last` are different, `x` and `x_last` form a
    # bracket.
    x_last = xp.concat((x[n:], x[:n]))
    f_last = xp.concat((f[n:], f[:n]))
    # `x0` is the "fixed" end of the bracket.
    x0 = x_last
    # We don't need to retain the corresponding function value, since the
    # fixed end of the bracket is only needed to compute the new value of the
    # moving end; it is never returned.
    limit = xp.concat((xmin, xmax))

    factor = xp_ravel(xp.broadcast_to(factor, shape), xp=xp)
    factor = xp.astype(factor, dtype, copy=False)
    factor = xp.concat((factor, factor))

    active = xp.arange(2*n)
    args = [xp.concat((arg, arg)) for arg in args]

    # This is needed due to inner workings of `eim._loop`.
    # We're abusing it a tiny bit.
    shape = shape + (2,)

    # `d` is for "distance".
    # For searches without a limit, the distance between the fixed end of the
    # bracket `x0` and the moving end `x` will grow by `factor` each iteration.
    # For searches with a limit, the distance between the `limit` and moving
    # end of the bracket `x` will shrink by `factor` each iteration.
    i = xp.isinf(limit)
    ni = ~i
    d = xp.zeros_like(x)
    d[i] = x[i] - x0[i]
    d[ni] = limit[ni] - x[ni]

    status = xp.full_like(x, eim._EINPROGRESS, dtype=xp.int32)  # in progress
    status[invalid_bracket] = eim._EINPUTERR
    nit, nfev = 0, 1  # one function evaluation per side performed above

    work = _RichResult(x=x, x0=x0, f=f, limit=limit, factor=factor,
                       active=active, d=d, x_last=x_last, f_last=f_last,
                       nit=nit, nfev=nfev, status=status, args=args,
                       xl=xp.nan, xr=xp.nan, fl=xp.nan, fr=xp.nan, n=n)
    res_work_pairs = [('status', 'status'), ('xl', 'xl'), ('xr', 'xr'),
                      ('nit', 'nit'), ('nfev', 'nfev'), ('fl', 'fl'),
                      ('fr', 'fr'), ('x', 'x'), ('f', 'f'),
                      ('x_last', 'x_last'), ('f_last', 'f_last')]

    def pre_func_eval(work):
        # Initialize moving end of bracket
        x = xp.zeros_like(work.x)

        # Unlimited brackets grow by `factor` by increasing distance from fixed
        # end to moving end.
        i = xp.isinf(work.limit)  # indices of unlimited brackets
        work.d[i] *= work.factor[i]
        x[i] = work.x0[i] + work.d[i]

        # Limited brackets grow by decreasing the distance from the limit to
        # the moving end.
        ni = ~i  # indices of limited brackets
        work.d[ni] /= work.factor[ni]
        x[ni] = work.limit[ni] - work.d[ni]

        return x

    def post_func_eval(x, f, work):
        # Keep track of the previous location of the moving end so that we can
        # return a narrower bracket. (The alternative is to remember the
        # original fixed end, but then the bracket would be wider than needed.)
        work.x_last = work.x
        work.f_last = work.f
        work.x = x
        work.f = f

    def check_termination(work):
        # Condition 0: initial bracket is invalid
        stop = (work.status == eim._EINPUTERR)

        # Condition 1: a valid bracket (or the root itself) has been found
        sf = xp.sign(work.f)
        sf_last = xp.sign(work.f_last)
        i = ((sf_last == -sf) | (sf_last == 0) | (sf == 0)) & ~stop
        work.status[i] = eim._ECONVERGED
        stop[i] = True

        # Condition 2: the other side's search found a valid bracket.
        # (If we just found a bracket with the rightward search, we can stop
        #  the leftward search, and vice-versa.)
        # To do this, we need to set the status of the other side's search;
        # this is tricky because `work.status` contains only the *active*
        # elements, so we don't immediately know the index of the element we
        # need to set - or even if it's still there. (That search may have
        # terminated already, e.g. by reaching its `limit`.)
        # To facilitate this, `work.active` contains a unit integer index of
        # each search. Index `k` (`k < n)` and `k + n` correspond with a
        # leftward and rightward search, respectively. Elements are removed
        # from `work.active` just as they are removed from `work.status`, so
        # we use `work.active` to help find the right location in
        # `work.status`.
        # Get the integer indices of the elements that can also stop
        also_stop = (work.active[i] + work.n) % (2*work.n)
        # Check whether they are still active. We want to find the indices
        # in work.active where the associated values in work.active are
        # contained in also_stop. xp.searchsorted let's us take advantage
        # of work.active being sorted, but requires some hackery because
        # searchsorted solves the separate but related problem of finding
        # the indices where the values in also_stop should be added to
        # maintain sorted order.
        j = xp.searchsorted(work.active, also_stop)
        # If the location exceeds the length of the `work.active`, they are
        # not there. This happens when a value in also_stop is larger than
        # the greatest value in work.active. This case needs special handling
        # because we cannot simply check that also_stop == work.active[j].
        mask = j < work.active.shape[0]
        # Note that we also have to use the mask to filter also_stop to ensure
        # that also_stop and j will still have the same shape.
        j, also_stop = j[mask], also_stop[mask]
        j = j[also_stop == work.active[j]]
        # Now convert these to boolean indices to use with `work.status`.
        i = xp.zeros_like(stop)
        i[j] = True  # boolean indices of elements that can also stop
        i = i & ~stop
        work.status[i] = _ESTOPONESIDE
        stop[i] = True

        # Condition 3: moving end of bracket reaches limit
        i = (work.x == work.limit) & ~stop
        work.status[i] = _ELIMITS
        stop[i] = True

        # Condition 4: non-finite value encountered
        i = ~(xp.isfinite(work.x) & xp.isfinite(work.f)) & ~stop
        work.status[i] = eim._EVALUEERR
        stop[i] = True

        return stop

    def post_termination_check(work):
        pass

    def customize_result(res, shape):
        n = res['x'].shape[0] // 2

        # To avoid ambiguity, below we refer to `xl0`, the initial left endpoint
        # as `a` and `xr0`, the initial right endpoint, as `b`.
        # Because we treat the two one-sided searches as though they were
        # independent, what we keep track of in `work` and what we want to
        # return in `res` look quite different. Combine the results from the
        # two one-sided searches before reporting the results to the user.
        # - "a" refers to the leftward search (the moving end started at `a`)
        # - "b" refers to the rightward search (the moving end started at `b`)
        # - "l" refers to the left end of the bracket (closer to -oo)
        # - "r" refers to the right end of the bracket (closer to +oo)
        xal = res['x'][:n]
        xar = res['x_last'][:n]
        xbl = res['x_last'][n:]
        xbr = res['x'][n:]

        fal = res['f'][:n]
        far = res['f_last'][:n]
        fbl = res['f_last'][n:]
        fbr = res['f'][n:]

        # Initialize the brackets and corresponding function values to return
        # to the user. Brackets may not be valid (e.g. there is no root,
        # there weren't enough iterations, NaN encountered), but we still need
        # to return something. One option would be all NaNs, but what I've
        # chosen here is the left- and right-most points at which the function
        # has been evaluated. This gives the user some information about what
        # interval of the real line has been searched and shows that there is
        # no sign change between the two ends.
        xl = xp.asarray(xal, copy=True)
        fl = xp.asarray(fal, copy=True)
        xr = xp.asarray(xbr, copy=True)
        fr = xp.asarray(fbr, copy=True)

        # `status` indicates whether the bracket is valid or not. If so,
        # we want to adjust the bracket we return to be the narrowest possible
        # given the points at which we evaluated the function.
        # For example if bracket "a" is valid and smaller than bracket "b" OR
        # if bracket "a" is valid and bracket "b" is not valid, we want to
        # return bracket "a" (and vice versa).
        sa = res['status'][:n]
        sb = res['status'][n:]

        da = xar - xal
        db = xbr - xbl

        i1 = ((da <= db) & (sa == 0)) | ((sa == 0) & (sb != 0))
        i2 = ((db <= da) & (sb == 0)) | ((sb == 0) & (sa != 0))

        xr[i1] = xar[i1]
        fr[i1] = far[i1]
        xl[i2] = xbl[i2]
        fl[i2] = fbl[i2]

        # Finish assembling the result object
        res['xl'] = xl
        res['xr'] = xr
        res['fl'] = fl
        res['fr'] = fr

        res['nit'] = xp.maximum(res['nit'][:n], res['nit'][n:])
        res['nfev'] = res['nfev'][:n] + res['nfev'][n:]
        # If the status on one side is zero, the status is zero. In any case,
        # report the status from one side only.
        res['status'] = xp.where(sa == 0, sa, sb)
        res['success'] = (res['status'] == 0)

        del res['x']
        del res['f']
        del res['x_last']
        del res['f_last']

        return shape[:-1]

    return eim._loop(work, callback, shape, maxiter, func, args, dtype,
                     pre_func_eval, post_func_eval, check_termination,
                     post_termination_check, customize_result, res_work_pairs,
                     xp)


def _bracket_root(*args, **kwargs):
    res = bracket_root(*args, **kwargs)
    res.xl, res.xr = res.bracket
    res.fl, res.fr = res.f_bracket
    del res.bracket
    del res.f_bracket
    return res


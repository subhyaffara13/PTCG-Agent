import logging

def _initialize(g=globals()):
    "Set up global resource manager (deliberately not state-saved)"
    manager = ResourceManager()
    g['_manager'] = manager
    g.update(
        (name, getattr(manager, name))
        for name in dir(manager)
        if not name.startswith('_')
    )


def _initialize(g=globals()) -> None:
    "Set up global resource manager (deliberately not state-saved)"
    manager = ResourceManager()
    g['_manager'] = manager
    g.update(
        (name, getattr(manager, name))
        for name in dir(manager)
        if not name.startswith('_')
    )


def _initialize(func, xs, args, kwargs=None,
                complex_ok=False, preserve_shape=None, xp=None):
    """Initialize abscissa, function, and args arrays for elementwise function

    Parameters
    ----------
    func : callable
        An elementwise function with signature

            func(x: ndarray, *args) -> ndarray

        where each element of ``x`` is a finite real and ``args`` is a tuple,
        which may contain an arbitrary number of arrays that are broadcastable
        with ``x``.
    xs : tuple of arrays
        Finite real abscissa arrays. Must be broadcastable.
    args : tuple, optional
        Additional positional arguments to be passed to `func`.
    kwargs : tuple, optional
        Additional keyword arguments to be passed to `func`.
    preserve_shape : bool, default:False
        When ``preserve_shape=False`` (default), `func` may be passed
        arguments of any shape; `_scalar_optimization_loop` is permitted
        to reshape and compress arguments at will. When
        ``preserve_shape=False``, arguments passed to `func` must have shape
        `shape` or ``shape + (n,)``, where ``n`` is any integer.
    xp : namespace
        Namespace of array arguments in `xs`.

    Returns
    -------
    xs, fs, args : tuple of arrays
        Broadcasted, writeable, 1D abscissa and function value arrays (or
        NumPy floats, if appropriate). The dtypes of the `xs` and `fs` are
        `xfat`; the dtype of the `args` are unchanged.
    shape : tuple of ints
        Original shape of broadcasted arrays.
    xfat : NumPy dtype
        Result dtype of abscissae, function values, and args determined using
        `np.result_type`, except integer types are promoted to `np.float64`.

    Raises
    ------
    ValueError
        If the result dtype is not that of a real scalar

    Notes
    -----
    Useful for initializing the input of SciPy functions that accept
    an elementwise callable, abscissae, and arguments; e.g.
    `scipy.optimize._chandrupatla`.
    """
    nx = len(xs)
    xp = array_namespace(*xs) if xp is None else xp

    if kwargs is not None:
        args = (*args, *kwargs.values())
        kwnames = tuple(kwargs.keys())
        def func(x, *args, kwnames=kwnames, func=func, **kwargs):
            nargs = len(args) - len(kwnames)
            kwarrays = dict(zip(kwnames, args[nargs:]))
            return func(x, *args[:nargs], **kwarrays, **kwargs)

    # Try to preserve `dtype`, but we need to ensure that the arguments are at
    # least floats before passing them into the function; integers can overflow
    # and cause failure.
    # There might be benefit to combining the `xs` into a single array and
    # calling `func` once on the combined array. For now, keep them separate.
    xat = xp_result_type(*xs, force_floating=True, xp=xp)
    xas = xp.broadcast_arrays(*xs, *args)  # broadcast and rename
    xs, args = xas[:nx], xas[nx:]
    xs = [xp.asarray(x, dtype=xat) for x in xs]  # use copy=False when implemented
    fs = [xp.asarray(func(x, *args)) for x in xs]
    shape = xs[0].shape
    fshape = fs[0].shape

    if preserve_shape:
        # bind original shape/func now to avoid late-binding gotcha
        def func(x, *args, shape=shape, func=func,  **kwargs):
            i = (0,)*(len(fshape) - len(shape))
            return func(x[i], *args, **kwargs)
        shape = np.broadcast_shapes(fshape, shape)  # just shapes; use of NumPy OK
        xs = [xp.broadcast_to(x, shape) for x in xs]
        args = [xp.broadcast_to(arg, shape) for arg in args]

    message = ("The shape of the array returned by `func` must be the same as "
               "the broadcasted shape of `x` and all other `args`.")
    if preserve_shape is not None:  # only in tanhsinh for now
        message = f"When `preserve_shape=False`, {message.lower()}"
    shapes_equal = [f.shape == shape for f in fs]
    if not all(shapes_equal):  # use Python all to reduce overhead
        raise ValueError(message)

    # These algorithms tend to mix the dtypes of the abscissae and function
    # values, so figure out what the result will be and convert them all to
    # that type from the outset.
    xfat = xp.result_type(*([f.dtype for f in fs] + [xat]))
    if not complex_ok and not xp.isdtype(xfat, "real floating"):
        raise ValueError("Abscissae and function output must be real numbers.")
    xs = [xp.asarray(x, dtype=xfat, copy=True) for x in xs]
    fs = [xp.asarray(f, dtype=xfat, copy=True) for f in fs]

    # To ensure that we can do indexing, we'll work with at least 1d arrays,
    # but remember the appropriate shape of the output.
    xs = [xp.reshape(x, (-1,)) for x in xs]
    fs = [xp.reshape(f, (-1,)) for f in fs]
    args = [xp.reshape(xp.asarray(arg, copy=True), (-1,)) for arg in args]
    return func, xs, fs, args, shape, xfat, xp


def _initialize(state, env):
    configuration = env.configuration
    num_agents = len(state)
    obs0 = state[0].observation

    seed = resolve_episode_seed(env)

    board_size = int(get(configuration, "boardSize", 10))
    starting_money = int(get(configuration, "startingMoney", 3000))

    farms = [_new_farm(board_size, starting_money) for _ in range(num_agents)]
    privates = [_new_private() for _ in range(num_agents)]
    market_overrides = get(configuration, "marketParams", None)
    resolved_params = _resolve_market_params(market_overrides) if market_overrides else None
    market = _new_market(resolved_params)
    town = _new_town()

    obs0.farms = farms
    obs0.market = market
    obs0.town = town
    obs0.day = 0
    obs0.hour = 0

    for i in range(num_agents):
        state[i].observation.player = i
        state[i].observation.private = privates[i]
        if i > 0:
            state[i].observation.farms = farms
            state[i].observation.market = market
            state[i].observation.town = town
            state[i].observation.day = 0
            state[i].observation.hour = 0


def _initialize(state, env):
    configuration = env.configuration
    num_agents = len(state)
    obs0 = state[0].observation

    board_size = int(get(configuration, "boardSize", 5))
    starting_money = int(get(configuration, "startingMoney", 150))

    farms = [_new_farm(board_size, starting_money) for _ in range(num_agents)]
    obs0.farms = farms
    obs0.day = 0
    obs0.hour = 0
    for i in range(num_agents):
        state[i].observation.player = i
        if i > 0:
            state[i].observation.farms = farms
            state[i].observation.day = 0
            state[i].observation.hour = 0


def _initialize():
  """Initializes loggers and handlers."""
  global _absl_logger, _absl_handler

  if _absl_logger:
    return

  original_logger_class = logging.getLoggerClass()
  logging.setLoggerClass(ABSLLogger)
  _absl_logger = logging.getLogger('absl')
  logging.setLoggerClass(original_logger_class)

  python_logging_formatter = PythonFormatter()
  _absl_handler = ABSLHandler(python_logging_formatter)


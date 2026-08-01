
def init(autoreset=False, convert=None, strip=None, wrap=True):

    if not wrap and any([autoreset, convert, strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')

    global wrapped_stdout, wrapped_stderr
    global orig_stdout, orig_stderr

    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    if sys.stdout is None:
        wrapped_stdout = None
    else:
        sys.stdout = wrapped_stdout = \
            wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    if sys.stderr is None:
        wrapped_stderr = None
    else:
        sys.stderr = wrapped_stderr = \
            wrap_stream(orig_stderr, convert, strip, autoreset, wrap)

    global atexit_done
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def init() -> bool:
    """
    Explicitly initializes the Python Imaging Library. This function
    loads all available file format drivers.

    It is called when opening or saving images if :py:meth:`~preinit()` is
    insufficient, and by :py:meth:`~PIL.features.pilinfo`.
    """

    global _initialized
    if _initialized >= 2:
        return False

    for plugin in _plugins:
        try:
            logger.debug("Importing %s", plugin)
            __import__(f"{__spec__.parent}.{plugin}", globals(), locals(), [])
        except ImportError as e:  # noqa: PERF203
            logger.debug("Image: failed to import %s: %s", plugin, e)

    if OPEN or SAVE:
        _initialized = 2
        return True
    return False


def init(backend=None):
    global _is_init
    # select the camera module to import here.

    backends = [b.lower() for b in get_backends()]
    if not backends:
        raise error("No camera backends are supported on your platform!")

    backend = backends[0] if backend is None else backend.lower()
    if backend not in backends:
        warnings.warn(
            "We don't think this is a supported backend on this system, "
            "but we'll try it...",
            Warning,
            stacklevel=2,
        )

    try:
        _setup_backend(backend)
    except ImportError:
        emsg = f"Backend '{backend}' is not supported on your platform!"
        if backend in ("opencv", "opencv-mac", "videocapture"):
            dep = "vidcap" if backend == "videocapture" else "OpenCV"
            emsg += (
                f" Make sure you have '{dep}' installed to be able to use this backend"
            )

        raise error(emsg)

    _is_init = True


def init():
    """init() -> None
    initialize pygame.fastevent
    """
    global _ft_init
    if not pygame.display.get_init():
        raise error("video system not initialized")

    register_quit(_quit_hook)
    _ft_init = True


def init():
    """initialize the midi module
    pygame.midi.init(): return None

    Call the initialisation function before using the midi module.

    It is safe to call this more than once.
    """
    if not _module_init():
        _pypm.Initialize()
        _module_init(True)
        atexit.register(quit)


def init():
    global vidcap
    try:
        import vidcap as vc
    except ImportError:
        from VideoCapture import vidcap as vc
    vidcap = vc


def init():
    r"""Initialize PyTorch's CUDA state.

    You may need to call this explicitly if you are interacting with
    PyTorch via its C API, as Python bindings for CUDA functionality
    will not be available until this initialization takes place.
    Ordinary users should not need this, as all of PyTorch's CUDA methods
    automatically initialize CUDA state on-demand.

    Does nothing if the CUDA state is already initialized.
    """
    _lazy_init()


def init():
    _lazy_init()


def init() -> None:
    r"""Initialize PyTorch's XPU state.
    This is a Python API about lazy initialization that avoids initializing
    XPU until the first time it is accessed. Does nothing if the XPU state is
    already initialized.
    """
    _lazy_init()


def init():
    """Initializes the lazy Torchscript backend"""
    torch._C._lazy_ts_backend._init()


def init(number_of_workers=0):
    """Does a little test to see if threading is worth it.
      Sets up a global worker queue if it's worth it.

    Calling init() is not required, but is generally better to do.
    """
    global _wq, _use_workers

    if number_of_workers:
        _use_workers = number_of_workers
    else:
        _use_workers = benchmark_workers()

    # if it is best to use zero workers, then use that.
    _wq = WorkerQueue(_use_workers)


def init(capacity: chex.Numeric, experience: Experience) -> ReplayBufferState:
  """Initialise a replay buffer.

  Args:
    capacity (chex.Numeric, int): max size of the buffer
    experience (Experience): initial value

  Returns:
    ReplayBufferState: state of the buffer
  """
  # Set experience value to be empty.
  experience = jax.tree.map(jnp.empty_like, experience)
  # Broadcast to [add_batch_size, ...]
  experience = jax.tree.map(
      lambda x: jnp.broadcast_to(x[jnp.newaxis, ...], (capacity, *x.shape)),
      experience,
  )
  return ReplayBufferState(
      capacity=capacity,
      experience=experience,
      entry_index=jnp.array(0),
      is_full=jnp.array(False, dtype=jnp.bool),
  )


def init(
  fn: Callable[..., Any],
  mutable: CollectionFilter = True,
  flags: Mapping | None = None,
) -> Callable[..., Any]:
  """Functionalize a `Scope` function for initialization.

  Args:
    fn: a function taking a `Scope` as its first argument.
    mutable: the filter determining which variable collections are mutable.
    flags: internal flags.

  Returns:
    `fn` with the scope partially applied.
  """

  @functools.wraps(fn)
  def wrapper(rngs, *args, **kwargs) -> tuple[Any, VariableDict]:
    if not _is_valid_rng(rngs) and not _is_valid_rngs(rngs):
      raise ValueError(
        'First argument passed to an init function should be a '
        '``jax.PRNGKey`` or a dictionary mapping strings to '
        '``jax.PRNGKey``.'
      )
    if not isinstance(rngs, (dict, FrozenDict)):
      rngs = {'params': rngs}
    init_flags = {**(flags if flags is not None else {}), 'initializing': True}
    return apply(fn, mutable=mutable, flags=init_flags)(
      {}, *args, rngs=rngs, **kwargs
    )

  return wrapper


def init(
  fn: Callable[..., Any],
  module: Module,
  mutable: CollectionFilter = DenyList('intermediates'),
  capture_intermediates: bool | Callable[[Module, str], bool] = False,
) -> Callable[..., FrozenVariableDict | dict[str, Any]]:
  """Creates an init function to call ``fn`` with a bound module.

  Unlike ``Module.init`` this function returns a new function with the signature
  ``(rngs, *args, **kwargs) -> variables``.
  The rngs can be a dict of PRNGKeys or a single ```PRNGKey`` which is
  equivalent to passing a dict with one PRNGKey with the name "params".

  The init function that is returned can be directly composed with
  JAX transformations like ``jax.jit``::

    >>> class Foo(nn.Module):
    ...   def encode(self, x):
    ...     ...
    ...   def decode(self, x):
    ...     ...

    >>> def f(foo, x):
    ...   z = foo.encode(x)
    ...   y = foo.decode(z)
    ...   # ...
    ...   return y

    >>> foo = Foo()
    >>> f_jitted = jax.jit(nn.init(f, foo))
    >>> variables = f_jitted(jax.random.key(0), jnp.ones((1, 3)))

  Args:
    fn: The function that should be applied. The first argument passed will be
      a module instance of the ``module`` with variables and RNGs bound to it.
    module: The ``Module`` that will be used to bind variables and RNGs to. The
      ``Module`` passed as the first argument to ``fn`` will be a clone of
      module.
    mutable: Can be bool, str, or list. Specifies which collections should be
      treated as mutable: ``bool``: all/no collections are mutable. ``str``: The
      name of a single mutable collection. ``list``: A list of names of mutable
      collections. By default, all collections except "intermediates" are
      mutable.
    capture_intermediates: If `True`, captures intermediate return values of all
      Modules inside the "intermediates" collection. By default, only the return
      values of all `__call__` methods are stored. A function can be passed to
      change the filter behavior. The filter function takes the Module instance
      and method name and returns a bool indicating whether the output of that
      method invocation should be stored.

  Returns:
    The init function wrapping ``fn``.
  """
  init_fn = init_with_output(fn, module, mutable, capture_intermediates)

  @functools.wraps(init_fn)
  def init_wrapper(*args, **kwargs):
    return init_fn(*args, **kwargs)[1]

  return init_wrapper


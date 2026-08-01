
def apply(loop=None):
    """Patch asyncio to make its event loop reentrant."""
    _patch_asyncio()
    _patch_policy()
    _patch_tornado()

    loop = loop or asyncio.get_event_loop()
    _patch_loop(loop)


def apply(*func_and_args, **kwargs):
    """ Applies a function and returns the results

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> apply(double, 5)
    10

    >>> tuple(map(apply, [double, inc, double], [10, 500, 8000]))
    (20, 501, 16000)
    """
    if not func_and_args:
        raise TypeError('func argument is required')
    func, args = func_and_args[0], func_and_args[1:]
    return func(*args, **kwargs)


def apply(transform):
    def wrap(func):
        return functools.wraps(func)(compose(transform, func))

    return wrap


def apply(dist: Distribution, config: dict, filename: StrPath) -> Distribution:
    """Apply configuration dict read with :func:`read_configuration`"""

    if not config:
        return dist  # short-circuit unrelated pyproject.toml file

    root_dir = os.path.dirname(filename) or "."

    _apply_project_table(dist, config, root_dir)
    _apply_tool_table(dist, config, filename)

    current_directory = os.getcwd()
    os.chdir(root_dir)
    try:
        dist._finalize_requires()
        dist._finalize_license_expression()
        dist._finalize_license_files()
    finally:
        os.chdir(current_directory)

    return dist


def apply(transform):
    def wrap(func):
        return functools.wraps(func)(compose(transform, func))

    return wrap


def apply(transform):
    """
    Decorate a function with a transform function that is
    invoked on results returned from the decorated function.

    >>> @apply(reversed)
    ... def get_numbers(start):
    ...     "doc for get_numbers"
    ...     return range(start, start+3)
    >>> list(get_numbers(4))
    [6, 5, 4]
    >>> get_numbers.__doc__
    'doc for get_numbers'
    """

    def wrap(func):
        return functools.wraps(func)(compose(transform, func))

    return wrap


def apply(matrix: Array, vector: Array, inverse: bool = False) -> Array:
    xp = array_namespace(matrix)
    if vector.shape[-1] != 3:
        raise ValueError(f"Expected vector to have shape (..., 3), got {vector.shape}.")
    vec = xp.empty(
        (*vector.shape[:-1], 4), dtype=vector.dtype, device=xp_device(vector)
    )
    vec = xpx.at(vec)[..., :3].set(vector)
    vec = xpx.at(vec)[..., 3].set(1)
    vec = vec[..., None]

    if inverse:
        matrix = inv(matrix)

    # We raise a ValueError manually here because letting the function run its course
    # would raise heterogeneous error types and messages for different frameworks.
    # However, the error only mimics numpy's error message and does not provide the
    # same amount of context.
    if not broadcastable(matrix.shape, vec.shape):  # type:ignore[arg-type]
        raise ValueError("operands could not be broadcast together")
    return (matrix @ vec)[..., :3, 0]


def apply(quat: Array, points: Array, inverse: bool = False) -> Array:
    xp = array_namespace(quat)
    mat = as_matrix(quat)
    # We do not have access to einsum. To avoid broadcasting issues, we add a singleton
    # dimension to the points array and remove it after the operation.
    points = points[..., None]
    if not broadcastable(mat.shape, points.shape):
        raise ValueError(
            f"Cannot broadcast {quat.shape[:-1]} rotations to {points.shape[:-1]} "
            "vectors."
        )
    if inverse:
        # TODO: Replace with .mT once numpy 2.0 is the minimum supported version
        return (xp.matrix_transpose(mat) @ points)[..., 0]
    return (mat @ points)[..., 0]


def apply(
  fn: Callable[..., Any],
  mutable: CollectionFilter = False,
  flags: Mapping | None = None,
) -> Callable[..., Any]:
  """Functionalize a `Scope` function.

  Args:
    fn: a function taking a `Scope` as its first argument.
    mutable: the filter determining which variable collections are mutable.
    flags: internal flags.

  Returns:
    `fn` with the scope partially applied.
  """

  @functools.wraps(fn)
  def wrapper(
    variables: VariableDict,
    *args,
    rngs: PRNGKey | RNGSequences | None = None,
    **kwargs,
  ) -> Any | tuple[Any, VariableDict | dict[str, Any]]:
    if rngs is not None:
      if not _is_valid_rng(rngs) and not _is_valid_rngs(rngs):
        raise ValueError(
          'The ``rngs`` argument passed to an apply function should be a '
          '``jax.PRNGKey`` or a dictionary mapping strings to '
          '``jax.PRNGKey``.'
        )
      if not isinstance(rngs, (dict, FrozenDict)):
        rngs = {'params': rngs}

    # Try to detect if user accidentally passed {'params': {'params': ...}.
    if (
      'params' in variables
      and isinstance(variables['params'], (dict, FrozenDict))
      and 'params' in variables['params']
    ):
      raise errors.ApplyScopeInvalidVariablesStructureError(variables)

    with bind(
      variables, rngs=rngs, mutable=mutable, flags=flags
    ).temporary() as root:
      y = fn(root, *args, **kwargs)
    if mutable is not False:
      return y, root.mutable_variables()
    else:
      return y

  return wrapper


def apply(
  fn: Callable[..., Any],
  module: Module,
  mutable: CollectionFilter = False,
  capture_intermediates: bool | Callable[[Module, str], bool] = False,
) -> Callable[..., Any]:
  """Creates an apply function to call ``fn`` with a bound module.

  Unlike ``Module.apply`` this function returns a new function with the
  signature ``(variables, *args, rngs=None, **kwargs) -> T`` where ``T`` is the
  return type of ``fn``. If ``mutable`` is not ``False`` the return type is a
  tuple where the second item is a ``FrozenDict`` with the mutated variables.

  The apply function that is returned can be directly composed with
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

    >>> variables = {}
    >>> foo = Foo()
    >>> f_jitted = jax.jit(nn.apply(f, foo))
    >>> f_jitted(variables, jnp.ones((1, 3)))

  Args:
    fn: The function that should be applied. The first argument passed will be
      a module instance of the ``module`` with variables and RNGs bound to it.
    module: The ``Module`` that will be used to bind variables and RNGs to. The
      ``Module`` passed as the first argument to ``fn`` will be a clone of
      module.
    mutable: Can be bool, str, or list. Specifies which collections should be
      treated as mutable: ``bool``: all/no collections are mutable. ``str``: The
      name of a single mutable collection. ``list``: A list of names of mutable
      collections.
    capture_intermediates: If ``True``, captures intermediate return values of all
      Modules inside the "intermediates" collection. By default, only the return
      values of all `__call__` methods are stored. A function can be passed to
      change the filter behavior. The filter function takes the Module instance
      and method name and returns a bool indicating whether the output of that
      method invocation should be stored.

  Returns:
    The apply function wrapping ``fn``.
  """

  @functools.wraps(fn)
  def scope_fn(scope, *args, **kwargs):
    _context.capture_stack.append(capture_intermediates)
    try:
      return fn(module.clone(parent=scope, _deep_clone=True), *args, **kwargs)
    finally:
      _context.capture_stack.pop()

  if capture_intermediates is True:  # pylint: disable=g-bool-id-comparison
    capture_intermediates = capture_call_intermediates
  if capture_intermediates:
    mutable = union_filters(mutable, 'intermediates')
  return core.apply(scope_fn, mutable=mutable)


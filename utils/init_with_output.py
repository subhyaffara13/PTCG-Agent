
def init_with_output(
  fn: Callable[..., Any],
  module: Module,
  mutable: CollectionFilter = DenyList('intermediates'),
  capture_intermediates: bool | Callable[[Module, str], bool] = False,
) -> Callable[..., tuple[Any, FrozenVariableDict | dict[str, Any]]]:
  """Creates an init function to call ``fn`` with a bound module that also returns the function outputs.

  Unlike ``Module.init_with_output`` this function returns a new function with
  the signature ``(rngs, *args, **kwargs) -> (T, variables)`` where ``T`` is the
  return type of ``fn``. The rngs can be a dict of PRNGKeys or a single
  ```PRNGKey`` which is equivalent to passing a dict with one PRNGKey with the
  name "params".

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
    >>> f_jitted = jax.jit(nn.init_with_output(f, foo))
    >>> y, variables = f_jitted(jax.random.key(0), jnp.ones((1, 3)))

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
    capture_intermediates: If ``True``, captures intermediate return values of all
      Modules inside the "intermediates" collection. By default, only the return
      values of all `__call__` methods are stored. A function can be passed to
      change the filter behavior. The filter function takes the Module instance
      and method name and returns a bool indicating whether the output of that
      method invocation should be stored.

  Returns:
    The init function wrapping ``fn``.
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
  return core.init(scope_fn, mutable=mutable)


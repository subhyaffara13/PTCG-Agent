
def _resolve_bound_callable(
  f: tp.Callable[..., tp.Any],
) -> tuple[tp.Callable[..., tp.Any], tp.Any | None, bool]:
  """Detects and extracts bound methods from NNX Module callables.

  This function unwraps functools.partial layers to reach the underlying
  callable before checking if it's a bound method of an NNX Module.

  Args:
    f: A callable that may be a bound method of an NNX Module, potentially
       wrapped in functools.partial.

  Returns:
    A tuple of (unbound_fn, bound_self, was_bound) where:
    - unbound_fn: The unbound function (or original if not bound)
    - bound_self: The Module instance if f was bound, None otherwise
    - was_bound: True if f was a bound method, False otherwise

  Note:
    Preserves functools.partial wrappers around the callable and follows
    the same detection pattern as _get_unbound_fn in bridge/module.py.
    Detection occurs before any argnum shifting or index normalization.
  """
  # Unwrap functools.partial layers to reach the underlying callable.
  partials: list[tuple[tuple[tp.Any, ...], dict[str, tp.Any] | None]] = []
  g = f
  while isinstance(g, functools.partial):  # type: ignore[arg-type]
    partials.append((g.args or (), g.keywords))  # type: ignore[attr-defined]
    g = g.func  # type: ignore[attr-defined]

  bound_self = getattr(g, "__self__", None)
  was_bound = bool(inspect.ismethod(g) and isinstance(bound_self, Module))
  if was_bound:
    g = g.__func__  # type: ignore[attr-defined]

  # Reapply partials in reverse unwrap order.
  for args, kwargs in reversed(partials):
    kwargs = {} if kwargs is None else kwargs
    g = functools.partial(g, *args, **kwargs)

  return g, (bound_self if was_bound else None), was_bound



def register_static(cls: type[H]) -> type[H]:
  """Registers `cls` as a pytree with no leaves.

  Instances are treated as static by :func:`jax.jit`, :func:`jax.pmap`, etc. This can
  be an alternative to labeling inputs as static using ``jit``'s ``static_argnums``
  and ``static_argnames`` kwargs, ``pmap``'s ``static_broadcasted_argnums``, etc.

  Args:
    cls: type to be registered as static. Must be hashable, as defined in
      https://docs.python.org/3/glossary.html#term-hashable.

  Returns:
    The input class ``cls`` is returned unchanged after being added to JAX's
    pytree registry. This allows ``register_static`` to be used as a decorator.

  Examples:
    >>> import jax
    >>> @jax.tree_util.register_static
    ... class StaticStr(str):
    ...   pass

    This static string can now be used directly in :func:`jax.jit`-compiled
    functions, without marking the variable static using ``static_argnums``:

    >>> @jax.jit
    ... def f(x, y, s):
    ...   return x + y if s == 'add' else x - y
    ...
    >>> f(1, 2, StaticStr('add'))
    Array(3, dtype=int32, weak_type=True)
  """
  flatten = lambda obj: ((), obj)
  unflatten = lambda obj, empty_iter_children: obj
  register_pytree_with_keys(cls, flatten, unflatten)
  return cls


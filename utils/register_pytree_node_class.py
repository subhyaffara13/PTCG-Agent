
def register_pytree_node_class(cls: Typ) -> Typ:
  """Extends the set of types that are considered internal nodes in pytrees.

  This function is a thin wrapper around ``register_pytree_node``, and provides
  a class-oriented interface.

  Args:
    cls: a type to register as a pytree

  Returns:
    The input class ``cls`` is returned unchanged after being added to JAX's pytree
    registry. This return value allows ``register_pytree_node_class`` to be used as
    a decorator.

  See also:
    - :func:`~jax.tree_util.register_static`: simpler API for registering a static pytree.
    - :func:`~jax.tree_util.register_dataclass`: simpler API for registering a dataclass.
    - :func:`~jax.tree_util.register_pytree_node`
    - :func:`~jax.tree_util.register_pytree_with_keys`
    - :func:`~jax.tree_util.register_pytree_with_keys_class`

  Examples:
    Here we'll define a custom container that will be compatible with :func:`jax.jit`
    and other JAX transformations:

    >>> import jax
    >>> @jax.tree_util.register_pytree_node_class
    ... class MyContainer:
    ...   def __init__(self, x, y):
    ...     self.x = x
    ...     self.y = y
    ...   def tree_flatten(self):
    ...     return ((self.x, self.y), None)
    ...   @classmethod
    ...   def tree_unflatten(cls, aux_data, children):
    ...     return cls(*children)
    ...
    >>> m = MyContainer(jnp.zeros(4), jnp.arange(4))
    >>> def f(m):
    ...   return m.x + 2 * m.y
    >>> jax.jit(f)(m)
    Array([0., 2., 4., 6.], dtype=float32)
  """
  register_pytree_node(
    cls,
    op.methodcaller("tree_flatten"),
    cls.tree_unflatten  # pyrefly: ignore[missing-attribute]
  )
  return cls



def register_pytree_with_keys_class(cls: Typ) -> Typ:
  """Extends the set of types that are considered internal nodes in pytrees.

  This function is similar to ``register_pytree_node_class``, but requires a
  class that defines how it could be flattened with keys.

  It is a thin wrapper around ``register_pytree_with_keys``, and
  provides a class-oriented interface:

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
    - :func:`~jax.tree_util.register_pytree_node_class`

  Examples:
    >>> from jax.tree_util import register_pytree_with_keys_class, GetAttrKey
    >>> @register_pytree_with_keys_class
    ... class Special:
    ...   def __init__(self, x, y):
    ...     self.x = x
    ...     self.y = y
    ...   def tree_flatten_with_keys(self):
    ...     return (((GetAttrKey('x'), self.x), (GetAttrKey('y'), self.y)), None)
    ...   @classmethod
    ...   def tree_unflatten(cls, aux_data, children):
    ...     return cls(*children)
  """
  flatten_func = (
      op.methodcaller("tree_flatten") if hasattr(cls, "tree_flatten") else None
  )
  register_pytree_with_keys(
      cls, op.methodcaller("tree_flatten_with_keys"),
      cls.tree_unflatten,  # pyrefly: ignore[missing-attribute]
      flatten_func
  )
  return cls


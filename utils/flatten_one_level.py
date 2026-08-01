
def flatten_one_level(tree: Any) -> tuple[Iterable[Any], Hashable]:
  """Flatten the given pytree node by one level.

  Args:
    tree: A valid pytree node, either built-in or registered via
      :func:`register_pytree_node` or related functions.

  Returns:
    A pair of the pytrees flattened children and its hashable metadata.

  Raises:
    ValueError: If the given pytree is not a built-in or registered container
    via ``register_pytree_node`` or ``register_pytree_with_keys``.

  Examples:
    >>> import jax
    >>> from jax._src.tree_util import flatten_one_level
    >>> flattened, meta = flatten_one_level({'a': [1, 2], 'b': {'c': 3}})
    >>> flattened
    ([1, 2], {'c': 3})
    >>> meta
    ('a', 'b')
  """
  out = default_registry.flatten_one_level(tree)
  if out is None:
    raise ValueError(f"can't tree-flatten type: {type(tree)}")
  else:
    return out


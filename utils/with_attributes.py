
def with_attributes(
  node: A,
  /,
  *,
  only: filterlib.Filter = ...,
  raise_if_not_found: bool = True,
  graph: bool | None = None,
  **attributes: tp.Any,
) -> A:
  """Creates a new node with attributes updated according to ``**attributes``.

  The new node contains references to jax arrays in the original node. Unlike
  ``set_attributes``, this function does not modify the original node.

  Example::
    >>> from flax import nnx
    ...
    >>> class Block(nnx.Module):
    ...   def __init__(self, din, dout, *, rngs: nnx.Rngs):
    ...     self.linear = nnx.Linear(din, dout, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.5, deterministic=False)
    ...     self.batch_norm = nnx.BatchNorm(10, use_running_average=False, rngs=rngs)
    ...
    >>> block = Block(2, 5, rngs=nnx.Rngs(0))
    >>> block.dropout.deterministic, block.batch_norm.use_running_average
    (False, False)
    >>> new_block = nnx.with_attributes(block, deterministic=True, use_running_average=True)
    >>> new_block.dropout.deterministic, new_block.batch_norm.use_running_average
    (True, True)
    >>> block.dropout.deterministic, block.batch_norm.use_running_average
    (False, False)

  ``Filter``'s can be used to set the attributes of specific Modules::
    >>> block = Block(2, 5, rngs=nnx.Rngs(0))
    >>> new_block = nnx.with_attributes(block, only=nnx.Dropout, deterministic=True)
    >>> # Only the dropout will be modified
    >>> new_block.dropout.deterministic, new_block.batch_norm.use_running_average
    (True, False)

  Args:
    node: the object to create a copy of.
    only: Filters to select the Modules to set the attributes of.
    raise_if_not_found: If True (default), raises a ValueError if at least one
      attribute instance is not found in one of the selected Modules.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
    **attributes: The attributes to set.
  """
  predicate = filterlib.to_predicate(only)
  remaining_attributes = set(attributes.keys())

  def _set_attributes_fn(path, node):
    if isinstance(node, Module) and predicate(path, node):
      for name, value in attributes.items():
        if hasattr(node, name):
          setattr(node, name, value)
          remaining_attributes.discard(name)
    return node

  out = graphlib.recursive_map(_set_attributes_fn, node, graph=graph)

  if remaining_attributes and raise_if_not_found:
    raise ValueError(
      'Could not find at least one instance of the '
      f'following attributes: {sorted(remaining_attributes)}'
    )

  return out



def iter_children(
  node: tp.Any, /, *, graph: bool | None = None,
) -> tp.Iterator[tuple[Key, tp.Any]]:
  """Iterates over all immediate child nodes of a given node. This
  function is similar to :func:`iter_graph`, except it only iterates over the
  immediate children, and does not recurse further down.

  Specifically, this function creates a generator that yields the key and the
  child node instance, where the key is a string representing the attribute
  name to access the corresponding child.

  Example::

    >>> from flax import nnx
    ...
    >>> class SubModule(nnx.Module):
    ...   def __init__(self, din, dout, rngs):
    ...     self.linear1 = nnx.Linear(din, dout, rngs=rngs)
    ...     self.linear2 = nnx.Linear(din, dout, rngs=rngs)
    ...
    >>> class Block(nnx.Module):
    ...   def __init__(self, din, dout, *, rngs: nnx.Rngs):
    ...     self.linear = nnx.Linear(din, dout, rngs=rngs)
    ...     self.submodule = SubModule(din, dout, rngs=rngs)
    ...     self.dropout = nnx.Dropout(0.5)
    ...     self.batch_norm = nnx.BatchNorm(10, rngs=rngs)
    ...
    >>> model = Block(2, 5, rngs=nnx.Rngs(0))
    >>> for path, module in nnx.iter_children(model):
    ...  print(path, type(module).__name__)
    ...
    batch_norm BatchNorm
    dropout Dropout
    linear Linear
    submodule SubModule

  Args:
    node: A graph node object.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  if graph:
    node_impl = get_node_impl(node)
    if node_impl is None:
      raise ValueError(
        f'Expected a graph node, got {type(node).__name__}. '
        'If this is a regular pytree, use graph=False.'
      )
    node_dict = node_impl.node_dict(node)
    for key, value in node_dict.items():
      if is_graph_node(value):
        yield key, value
  else:
    _check_valid_pytree(node, 'iter_children')
    if not is_pytree_node(node, check_graph_registry=False):
      raise ValueError(
        f'Expected a pytree node, got {type(node).__name__}. '
        'If this is a graph node, use graph=True.'
      )
    children, _ = jax.tree_util.tree_flatten_with_path(
      node, is_leaf=lambda x: x is not node
    )
    for jax_key_path, child in children:
      if is_graph_node(child):
        key = _key_path_to_key(jax_key_path[0])
        yield key, child


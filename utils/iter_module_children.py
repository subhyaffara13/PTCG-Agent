
def iter_module_children(
  node: tp.Any, /, *, graph: bool | None = None,
) -> tp.Iterator[tuple[Key, tp.Any]]:
  """Iterates over all module children of a given node. This function is similar
  to :func:`iter_children`, except it only iterates over the module children
  only.

  Example::

    >>> from flax import nnx
    ...
    >>> model = nnx.Linear(2, 5, rngs=nnx.Rngs(0))
    >>> for path, module in nnx.iter_module_children(model):
    ...  print(path, type(module).__name__)
    ...
    >>> for path, module in nnx.iter_children(model):
    ...  print(path, type(module).__name__)
    ...
    bias Param
    kernel Param

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
      if is_node_module(value):
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
      if is_node_module(child):
        key = _key_path_to_key(jax_key_path[0])
        yield key, child



def graphdef(
  node: tp.Any, /, *, graph: bool | None = None,
) -> GraphDef[tp.Any]:
  """Get the :class:`GraphDef` of the given graph node.

  Example usage::

    >>> from flax import nnx

    >>> model = nnx.Linear(2, 3, rngs=nnx.Rngs(0))
    >>> graphdef, _ = nnx.split(model)
    >>> assert graphdef == nnx.graphdef(model)

  Args:
    node: A graph node object.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  Returns:
    The :class:`GraphDef` of the :class:`Module` object.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  graphdef, _ = flatten(node, graph=graph)
  return graphdef


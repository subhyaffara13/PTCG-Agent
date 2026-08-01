
def recursive_map(
  f: tp.Callable[[PathParts, tp.Any], tp.Any],
  node: tp.Any,
  /,
  *,
  graph: bool | None = None,
):
  """Recursively applies a function to all nodes and leaves of the given graph node.

  Example::

    >>> from flax import nnx
    >>> class MyModule(nnx.Module):
    ...   def __init__(self, *, rngs: nnx.Rngs):
    ...     self.lin = nnx.Linear(16, 16, rngs=rngs)
    ...     self.conv = nnx.Conv(16, 3, 1, 1, rngs=rngs)
    ...
    >>> def print_modules(path, node):
    ...   if isinstance(node, nnx.Module):
    ...     s = "." + ".".join(path)
    ...     print(f"Path = {s:<10}{node.__class__.__name__}")
    ...   return node
    ...
    >>> model = MyModule(rngs=nnx.Rngs(0))
    >>> new_model = nnx.recursive_map(print_modules, model)
    ...
    Path = .conv     Conv
    Path = .lin      Linear
    Path = .         MyModule

  Args:
    f: A function that takes a path and a node and returns a new node.
    node: A graph node object.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  if graph:
    node = clone(node, variables=False, graph=True)
    path_parts: PathParts = ()
    visited: set[int] = set()
    results: dict[int, tp.Any] = {}
    return _recursive_map_graph(f, node, path_parts, visited, results)
  else:
    return _recursive_map_tree(f, node)


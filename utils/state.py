
def state(node, /, *, graph: bool | None = None) -> State: ...


def state(node, first: filterlib.Filter, /, *, graph: bool | None = None) -> State: ...


def state(
  node,
  first: filterlib.Filter,
  second: filterlib.Filter,
  /,
  *filters: filterlib.Filter,
  graph: bool | None = None,
) -> tuple[State, ...]: ...


def state(
  node,
  *filters: filterlib.Filter,
  graph: bool | None = None,
) -> tp.Union[State, tuple[State, ...]]:
  """Similar to :func:`split` but only returns the :class:`State`'s indicated by the filters.

  Example usage::

    >>> from flax import nnx

    >>> class Model(nnx.Module):
    ...   def __init__(self, rngs):
    ...     self.batch_norm = nnx.BatchNorm(2, rngs=rngs)
    ...     self.linear = nnx.Linear(2, 3, rngs=rngs)
    ...   def __call__(self, x):
    ...     return self.linear(self.batch_norm(x))

    >>> model = Model(rngs=nnx.Rngs(0))
    >>> # get the learnable parameters from the batch norm and linear layer
    >>> params = nnx.state(model, nnx.Param)
    >>> # get the batch statistics from the batch norm layer
    >>> batch_stats = nnx.state(model, nnx.BatchStat)
    >>> # get them separately
    >>> params, batch_stats = nnx.state(model, nnx.Param, nnx.BatchStat)
    >>> # get them together
    >>> state = nnx.state(model)

  Args:
    node: A graph node object.
    *filters: One or more :class:`Variable` objects to filter by.
    graph: If ``True`` (default), uses graph-mode which supports the full
      NNX feature set including shared references. If ``False``, uses
      tree-mode which treats Modules as regular JAX pytrees, avoiding
      the overhead of the graph protocol.
  Returns:
    One or more :class:`State` mappings.
  """
  if graph is None:
    graph = set_graph_mode.current_value()
  _, flat_state = flatten(node, graph=graph)
  state = flat_state.to_nested_state()

  states: State | tuple[State, ...]
  if len(filters) == 0:
    states = state  # type: ignore[assignment]
  elif len(filters) == 1:
    states = statelib.filter_state(state, filters[0])
  else:
    states = statelib.filter_state(state, filters[0], filters[1], *filters[2:])

  return states



def graph_pop(
  node: tp.Any,
  filters: tuple[filterlib.Filter, ...],
) -> tuple[State, ...]:
  id_to_index: dict[int, Index] = {}
  path_parts: PathParts = ()
  predicates = tuple(filterlib.to_predicate(filter) for filter in filters)
  flat_states: tuple[dict[PathParts, LeafType], ...] = tuple(
    {} for _ in predicates
  )
  _graph_pop(node, id_to_index, path_parts, flat_states, predicates)
  return tuple(
    statelib.from_flat_state(flat_state) for flat_state in flat_states
  )


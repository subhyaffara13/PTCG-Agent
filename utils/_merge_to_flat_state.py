
def _merge_to_flat_state(states: tp.Iterable[tp.Any]):
  flat_state: list[tuple[PathParts, tp.Any]] = []

  for state in states:
    if isinstance(state, dict | State | GraphState):
      flat_state.extend(traversals.flatten_to_sequence(state))
    elif isinstance(state, FlatState):
      flat_state.extend(state)
    else:
      flat_state.append(((), state))

  flat_state.sort()
  return [value for _, value in flat_state]


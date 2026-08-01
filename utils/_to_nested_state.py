
def _to_nested_state(
  graphdef: GraphDef[A], flat_states: tp.Iterable[tp.Any]
) -> tuple[tp.Any, ...]:
  def _nested_or_leaf(flat_state):
    if not flat_state:
      return State({})
    if len(flat_state) == 1 and flat_state[0][0] == ():
      return flat_state[0][1]
    return statelib.from_flat_state(flat_state)
  states = tuple(
    _nested_or_leaf(flat_state) for flat_state in flat_states
  )
  return states



def _split_state(
  state: FlatState[tp.Any],
  filters: tuple[filterlib.Filter, ...],
) -> tuple[FlatState[tp.Any], tpe.Unpack[tuple[FlatState[tp.Any], ...]]]:
  if not filters:
    return (state,)  # type: ignore[bad-return-type]
  states = state.split(*filters)
  if not isinstance(states, tuple):
    return (states,)  # type: ignore[bad-return-type]
  assert len(states) > 0
  return states  # type: ignore[return-value]


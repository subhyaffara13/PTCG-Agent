
def _restore_dict(xs, states: dict[str, Any]) -> dict[str, Any]:
  diff = set(map(str, xs.keys())).difference(states.keys())
  if diff:
    raise ValueError(
      'The target dict keys and state dict keys do not match, target dict'
      f' contains keys {diff} which are not present in state dict at path'
      f' {current_path()}'
    )

  return {
    key: from_state_dict(value, states[str(key)], name=str(key))
    for key, value in xs.items()
  }



def _restore_frozen_dict(xs, states):
  diff = set(map(str, xs.keys())).difference(map(str, states.keys()))
  if diff:
    raise ValueError(
      'The target dict keys and state dict keys do not match, target dict'
      f' contains keys {diff} which are not present in state dict at path'
      f' {serialization.current_path()}'
    )

  return FrozenDict(
    {
      key: serialization.from_state_dict(value, states[str(key)], name=key)
      for key, value in xs.items()
    }
  )


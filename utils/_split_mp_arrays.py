
def _split_mp_arrays(
  target: dict[str, Any]
) -> tuple[dict[str, Any], list[tuple[MultiprocessArrayType, str]]]:
  """Split out the multiprocess arrays from the target pytree to save."""
  # When target is a single leaf instead of a pytree dict.
  if not isinstance(target, (core.FrozenDict, dict)):
    if _is_multiprocess_array(target):
      return MP_ARRAY_PH, [(target, '')]
    return target, []
  # Traverse the target and handle distributed arrays.
  flattened = traverse_util.flatten_dict(target, keep_empty_nodes=True)
  mpa_targets = []
  for key, value in flattened.items():
    if _is_multiprocess_array(value):
      subpath = '/'.join(key)
      mpa_targets.append((value, subpath))
      flattened[key] = MP_ARRAY_PH + subpath
  target = traverse_util.unflatten_dict(flattened)
  return target, mpa_targets


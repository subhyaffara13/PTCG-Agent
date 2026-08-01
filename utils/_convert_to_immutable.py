
def _convert_to_immutable(value, visit_map):
  """Convert Python built-in type to immutable, copying if necessary.

  Args:
    value: To be made immutable type (including its elements). Must have
        type list, tuple, or set.
    visit_map: As used elsewhere. See _frozenconfigdict_fill_seed()
        documentation.

  Returns:
    immutable_value: Immutable version of value, created with minimal
        copying.
    same_value: Whether the same value was returned untouched, i.e. with the
        same memory address. Boolean.
    visit_map: Updated visit_map.

  Raises:
    TypeError: If value is an invalid type (not a list, tuple, or set).
  """
  value_id = id(value)
  if value_id in visit_map:
    return visit_map[value_id], True, visit_map

  same_value = False
  if isinstance(value, set):
    immutable_value = frozenset(value)
  elif isinstance(value, tuple):
    immutable_value, same_value, visit_map = _tuple_to_immutable(
        value, visit_map)
  elif isinstance(value, list):
    immutable_value, _, visit_map = _tuple_to_immutable(tuple(value),
                                                        visit_map)
  else:
    # Type-check the input
    assert False
  visit_map[value_id] = immutable_value
  return immutable_value, same_value, visit_map


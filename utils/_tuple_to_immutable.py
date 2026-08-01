
def _tuple_to_immutable(value, visit_map):
  """Convert tuple to fully immutable tuple.

  Args:
    value: Tuple to be made fully immutable (including its elements).
    visit_map: As used elsewhere. See _frozenconfigdict_fill_seed()
        documentation. Must not contain id(value) as a key (if it does, an
        immutable version of value already exists).

  Returns:
    immutable_value: Immutable version of value, created with minimal
        copying (for example, if a value contains no mutable elements, it is
        returned untouched).
    same_value: Whether the same value was returned untouched, i.e. with the
        same memory address. Boolean.
    visit_map: Updated visit_map

  Raises:
    TypeError: If one of the following:
        1) value is not a tuple.
        2) value contains a dict, ConfigDict, or FieldReference. If it does,
           value is an invalid attribute of FrozenConfigDict, and this
           should have been caught in valid_input at initialization.
    ValueError: id(value) is in visit_map.
  """
  # Ensure there are no cycles
  assert id(value) not in visit_map

  value_copy = []
  same_value = True
  for element in value:
    # Sanity check: element cannot be dict, ConfigDict, or FieldReference
    assert not isinstance(element, (dict, ConfigDict, FieldReference))

    if isinstance(element, (list, tuple, set)):
      new_element, uncopied_element, visit_map = _convert_to_immutable(
          element, visit_map)
      same_value &= uncopied_element
      value_copy.append(new_element)
    else:
      value_copy.append(element)
  if same_value:
    return value, True, visit_map
  else:
    return tuple(value_copy), False, visit_map



def _SetStructValue(struct_value, value):
  if value is None:
    struct_value.null_value = 0
  elif isinstance(value, bool):
    # Note: this check must come before the number check because in Python
    # True and False are also considered numbers.
    struct_value.bool_value = value
  elif isinstance(value, str):
    struct_value.string_value = value
  elif isinstance(value, (int, float)):
    struct_value.number_value = value
  elif isinstance(value, (dict, Struct)):
    struct_value.struct_value.Clear()
    struct_value.struct_value.update(value)
  elif isinstance(value, (list, tuple, ListValue)):
    struct_value.list_value.Clear()
    struct_value.list_value.extend(value)
  else:
    raise ValueError('Unexpected type')



def _get_computed_value(value_or_fieldreference):
  if isinstance(value_or_fieldreference, FieldReference):
    return value_or_fieldreference.get()
  return value_or_fieldreference


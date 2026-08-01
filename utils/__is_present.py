
def _IsPresent(item):
  """Given a (FieldDescriptor, value) tuple from _fields, return true if the
  value should be included in the list returned by ListFields()."""

  if item[0].is_repeated:
    return bool(item[1])
  elif item[0].cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
    return item[1]._is_present_in_parent
  else:
    return True


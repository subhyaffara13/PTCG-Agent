
def _AddPropertiesForField(field, cls):
  """Adds a public property for a protocol message field.
  Clients can use this property to get and (in the case
  of non-repeated scalar fields) directly set the value
  of a protocol message field.

  Args:
    field: A FieldDescriptor for this field.
    cls: The class we're constructing.
  """
  # Catch it if we add other types that we should
  # handle specially here.
  assert _FieldDescriptor.MAX_CPPTYPE == 10

  constant_name = field.name.upper() + '_FIELD_NUMBER'
  setattr(cls, constant_name, field.number)

  if field.is_repeated:
    _AddPropertiesForRepeatedField(field, cls)
  elif field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
    _AddPropertiesForNonRepeatedCompositeField(field, cls)
  else:
    _AddPropertiesForNonRepeatedScalarField(field, cls)


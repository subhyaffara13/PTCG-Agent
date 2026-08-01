
def _IsMessageMapField(field):
  value_type = field.message_type.fields_by_name['value']
  return value_type.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE


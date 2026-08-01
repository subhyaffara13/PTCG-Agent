
def _IsMapField(field):
  return (field.type == _FieldDescriptor.TYPE_MESSAGE and
          field.message_type._is_map_entry)


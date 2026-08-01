
def _IsMapEntry(field):
  return (
      field.type == descriptor.FieldDescriptor.TYPE_MESSAGE
      and field.message_type.has_options
      and field.message_type.GetOptions().map_entry
  )


def _IsMapEntry(field):
  return (field.type == descriptor.FieldDescriptor.TYPE_MESSAGE and
          field.message_type.has_options and
          field.message_type.GetOptions().map_entry)


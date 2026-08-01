
def _IsValidPath(message_descriptor, path):
  """Checks whether the path is valid for Message Descriptor."""
  parts = path.split('.')
  last = parts.pop()
  for name in parts:
    field = message_descriptor.fields_by_name.get(name)
    if (field is None or
        field.is_repeated or
        field.type != FieldDescriptor.TYPE_MESSAGE):
      return False
    message_descriptor = field.message_type
  return last in message_descriptor.fields_by_name


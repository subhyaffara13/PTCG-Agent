
def _GetFieldByName(message_descriptor, field_name):
  """Returns a field descriptor by field name.

  Args:
    message_descriptor: A Descriptor describing all fields in message.
    field_name: The name of the field to retrieve.
  Returns:
    The field descriptor associated with the field name.
  """
  try:
    return message_descriptor.fields_by_name[field_name]
  except KeyError:
    raise ValueError('Protocol message %s has no "%s" field.' %
                     (message_descriptor.name, field_name))


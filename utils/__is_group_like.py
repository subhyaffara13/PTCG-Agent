
def _IsGroupLike(field):
  """Determines if a field is consistent with a proto2 group.

  Args:
    field: The field descriptor.

  Returns:
    True if this field is group-like, false otherwise.
  """
  # Groups are always tag-delimited.
  if field.type != descriptor.FieldDescriptor.TYPE_GROUP:
    return False

  # Group fields always are always the lowercase type name.
  if field.name != field.message_type.name.lower():
    return False

  if field.message_type.file != field.file:
    return False

  # Group messages are always defined in the same scope as the field.  File
  # level extensions will compare NULL == NULL here, which is why the file
  # comparison above is necessary to ensure both come from the same file.
  return (
      field.message_type.containing_type == field.extension_scope
      if field.is_extension
      else field.message_type.containing_type == field.containing_type
  )


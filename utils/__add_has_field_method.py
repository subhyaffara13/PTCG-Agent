
def _AddHasFieldMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""

  hassable_fields = {}
  for field in message_descriptor.fields:
    if field.is_repeated:
      continue
    # For proto3, only submessages and fields inside a oneof have presence.
    if not field.has_presence:
      continue
    hassable_fields[field.name] = field

  # Has methods are supported for oneof descriptors.
  for oneof in message_descriptor.oneofs:
    hassable_fields[oneof.name] = oneof

  def HasField(self, field_name):
    try:
      field = hassable_fields[field_name]
    except KeyError as exc:
      raise ValueError('Protocol message %s has no non-repeated field "%s" '
                       'nor has presence is not available for this field.' % (
                           message_descriptor.full_name, field_name)) from exc

    if isinstance(field, descriptor_mod.OneofDescriptor):
      try:
        return HasField(self, self._oneofs[field].name)
      except KeyError:
        return False
    else:
      if field.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
        value = self._fields.get(field)
        return value is not None and value._is_present_in_parent
      else:
        return field in self._fields

  cls.HasField = HasField


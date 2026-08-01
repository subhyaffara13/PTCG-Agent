
def _AddByteSizeMethod(message_descriptor, cls):
  """Helper for _AddMessageMethods()."""

  def ByteSize(self):
    if not self._cached_byte_size_dirty:
      return self._cached_byte_size

    size = 0
    descriptor = self.DESCRIPTOR
    if descriptor._is_map_entry:
      # Fields of map entry should always be serialized.
      key_field = descriptor.fields_by_name['key']
      _MaybeAddEncoder(cls, key_field)
      size = key_field._sizer(self.key)
      value_field = descriptor.fields_by_name['value']
      _MaybeAddEncoder(cls, value_field)
      size += value_field._sizer(self.value)
    else:
      for field_descriptor, field_value in self.ListFields():
        _MaybeAddEncoder(cls, field_descriptor)
        size += field_descriptor._sizer(field_value)
      for tag_bytes, value_bytes in self._unknown_fields:
        size += len(tag_bytes) + len(value_bytes)

    self._cached_byte_size = size
    self._cached_byte_size_dirty = False
    self._listener_for_children.dirty = False
    return size

  cls.ByteSize = ByteSize


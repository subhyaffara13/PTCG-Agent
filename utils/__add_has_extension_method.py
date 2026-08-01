
def _AddHasExtensionMethod(cls):
  """Helper for _AddMessageMethods()."""
  def HasExtension(self, field_descriptor):
    extension_dict._VerifyExtensionHandle(self, field_descriptor)
    if field_descriptor.is_repeated:
      raise KeyError('"%s" is repeated.' % field_descriptor.full_name)

    if field_descriptor.cpp_type == _FieldDescriptor.CPPTYPE_MESSAGE:
      value = self._fields.get(field_descriptor)
      return value is not None and value._is_present_in_parent
    else:
      return field_descriptor in self._fields
  cls.HasExtension = HasExtension


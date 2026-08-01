
def _AddClearExtensionMethod(cls):
  """Helper for _AddMessageMethods()."""
  def ClearExtension(self, field_descriptor):
    extension_dict._VerifyExtensionHandle(self, field_descriptor)

    # Similar to ClearField(), above.
    if field_descriptor in self._fields:
      del self._fields[field_descriptor]
    self._Modified()
  cls.ClearExtension = ClearExtension


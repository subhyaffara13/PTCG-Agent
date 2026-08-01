
def _AddPropertiesForFields(descriptor, cls):
  """Adds properties for all fields in this protocol message type."""
  for field in descriptor.fields:
    _AddPropertiesForField(field, cls)

  if descriptor.is_extendable:
    # _ExtensionDict is just an adaptor with no state so we allocate a new one
    # every time it is accessed.
    cls.Extensions = property(lambda self: _ExtensionDict(self))


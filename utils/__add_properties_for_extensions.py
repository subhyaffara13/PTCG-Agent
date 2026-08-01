
def _AddPropertiesForExtensions(descriptor, cls):
  """Adds properties for all fields in this protocol message type."""
  extensions = descriptor.extensions_by_name
  for extension_name, extension_field in extensions.items():
    constant_name = extension_name.upper() + '_FIELD_NUMBER'
    setattr(cls, constant_name, extension_field.number)

  # TODO: Migrate all users of these attributes to functions like
  #   pool.FindExtensionByNumber(descriptor).
  if descriptor.file is not None:
    # TODO: Use cls.MESSAGE_FACTORY.pool when available.
    pool = descriptor.file.pool


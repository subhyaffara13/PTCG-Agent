
def _AddClassAttributesForNestedExtensions(descriptor, dictionary):
  extensions = descriptor.extensions_by_name
  for extension_name, extension_field in extensions.items():
    assert extension_name not in dictionary
    dictionary[extension_name] = extension_field


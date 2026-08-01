
def _ismodule(obj: object) -> bool:
  # Do not use `isinstance` as it trigger `.__getattribute__('__class__')`
  # implemented by some lazy objects (like TFDS `LazyBuilderImport`)
  return issubclass(type(obj), types.ModuleType)


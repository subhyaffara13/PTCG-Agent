
def _fix_annotations(cls):
  """Remove the `_: dataclasses.KW_ONLY` annotation."""
  if cls is object or '_' not in getattr(cls, '__annotations__', {}):
    return
  old_annotations = dict(cls.__annotations__)
  cls.__annotations__.pop('_')
  return old_annotations


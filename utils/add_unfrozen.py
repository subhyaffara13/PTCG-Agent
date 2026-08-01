
def add_unfrozen(cls: _Cls) -> _Cls:
  """Add the `frozen`, `unfrozen` methods."""
  cls_frozen = getattr(cls, 'frozen', None)
  cls_unfrozen = getattr(cls, 'has_unfrozen', None)

  # Already inherit a unfrozeen class
  if cls_frozen is frozen and cls_unfrozen is unfrozen:
    return cls

  # Partial implementation, or collision detected
  if cls_frozen is not None or cls_unfrozen is not None:
    raise ValueError(f'{cls} already define `frozen` or `unfrozen`')

  cls.frozen = frozen
  cls.unfrozen = unfrozen

  return cls


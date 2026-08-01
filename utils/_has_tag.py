
def _has_tag(x: tp.Any) -> tp.TypeGuard[HasTag]:
  return hasattr(x, 'tag')



def _ensure_optional_axes(x: Axis) -> Axis:
  def force(x):
    if x is None:
      return None
    try:
      return operator.index(x)
    except TypeError:
      return tuple(i if isinstance(i, str) else operator.index(i) for i in x)
  return core.concrete_or_error(
    force, x, "The axis argument must be known statically.")


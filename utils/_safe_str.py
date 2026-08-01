
def _safe_str(obj: object) -> str:
  """Returns a string representation of an object."""
  try:
    return str(obj)
  except Exception:  # pylint: disable=broad-except
    return '<unprintable %s.%s object>' % (
        type(obj).__module__,
        type(obj).__name__,
    )


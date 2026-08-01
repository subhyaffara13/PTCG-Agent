
def _get_filepath_and_lineno(value) -> tuple[str, int] | tuple[None, None]:
  """Retrieves a filepath and line number for an inspectable value."""
  try:
    filepath = inspect.getsourcefile(value)
    if filepath is None:
      return None, None
    # This also returns the source lines, but we don't need those.
    _, lineno = inspect.findsource(value)
    # Add 1, since findsource is zero-indexed.
    return filepath, lineno + 1
  except (TypeError, OSError):
    return None, None


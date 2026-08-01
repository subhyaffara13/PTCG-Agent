
def has_keyword_arg(func: tp.Callable[..., tp.Any], name: str) -> bool:
  """Return True if func has keyword-only arguments with the given name."""
  return any(
    param.name == name
    and param.kind in (param.KEYWORD_ONLY, param.POSITIONAL_OR_KEYWORD)
    for param in inspect.signature(func).parameters.values()
  )


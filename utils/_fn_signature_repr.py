
def _fn_signature_repr(fn: Callable[..., Any]) -> str:
  """Constructs the signature representation of a function."""
  try:
    sig = inspect.Signature.from_callable(fn)
  except Exception:  # pylint: disable=broad-except
    # Many builtins do not expose any signature information
    return '...'

  parts = []
  is_first = True
  is_kwarg_only = False
  for param in sig.parameters.values():
    if not is_first:
      parts.append(', ')
    is_first = False
    if param.kind == inspect.Parameter.VAR_POSITIONAL:
      parts.append('*')
      is_kwarg_only = True
    elif param.kind == inspect.Parameter.VAR_KEYWORD:
      parts.append('**')
      is_kwarg_only = True
    elif param.kind == inspect.Parameter.KEYWORD_ONLY and not is_kwarg_only:
      is_kwarg_only = True
      parts.append('*, ')
    parts.append(param.name)
  return ''.join(parts)


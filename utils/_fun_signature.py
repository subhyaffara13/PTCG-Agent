
def _fun_signature(fun: tp.Callable) -> inspect.Signature | None:
  try:
    return inspect.signature(fun)
  except (ValueError, TypeError):
    return None


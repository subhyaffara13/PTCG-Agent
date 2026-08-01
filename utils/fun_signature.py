
def fun_signature(fun: Callable) -> inspect.Signature | None:
  try:
    return inspect.signature(fun)
  except (ValueError, TypeError):
    return None


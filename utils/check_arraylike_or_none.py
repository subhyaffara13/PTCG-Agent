
def check_arraylike_or_none(fun_name: str, *args: Any):
  assert isinstance(fun_name, str), f"fun_name must be a string. Got {fun_name}"
  if any(not (_arraylike(arg) or arg is None) for arg in args):
    pos, arg = next((i, arg) for i, arg in enumerate(args)
                    if not (_arraylike(arg) or arg is None))
    msg = "{} requires ndarray, scalar, or None arguments, got {} at position {}."
    raise TypeError(msg.format(fun_name, type(arg), pos))



def _validate_argnames(
    sig: inspect.Signature, argnames: tuple[str, ...], argnames_name: str
) -> None:
  """
  Validate that the argnames are sensible for a given function.

  For functions that accept a variable keyword arguments
  (`f(..., **kwargs)`) all argnames are considered valid except those
  marked as position-only (`f(pos_only, /, ...)`).
  """
  var_kwargs = False
  valid_kwargs: set[str] = set()
  invalid_kwargs: set[str] = set()
  for param_name, param in sig.parameters.items():
    if param.kind in _KEYWORD_ARGUMENTS:
      valid_kwargs.add(param_name)

    elif param.kind is inspect.Parameter.VAR_KEYWORD:
      var_kwargs = True

    elif param.kind in _INVALID_KEYWORD_ARGUMENTS:
      invalid_kwargs.add(param_name)

  # Check whether any kwargs are invalid due to position only
  if invalid_argnames := (invalid_kwargs & set(argnames)):
    raise ValueError(f"Jitted function has invalid argnames {invalid_argnames} "
                     f"in {argnames_name}. These are positional-only")

  # Takes any kwargs
  if var_kwargs:
    return

  # Check that all argnames exist on function
  if invalid_argnames := (set(argnames) - valid_kwargs):
    raise ValueError(f"Jitted function has invalid argnames {invalid_argnames} "
                     f"in {argnames_name}. Function does not take these args.")


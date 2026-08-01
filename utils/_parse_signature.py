
def _parse_signature(fn) -> _FnSignatureCache:
  """Parse the function signature."""
  # At this point, `ForwardRef` should have been resolved.
  try:
    hints = typing.get_type_hints(fn)
  except Exception as e:  # pylint: disable=broad-except
    epy.reraise(
        e,
        prefix=(
            f'Could not infer typing annotation of {fn.__qualname__} '
            f'defined in {fn.__module__}'
        ),
    )

  sig = inspect.signature(fn)

  # For each valid params, create the validator
  # TODO(py38): Use :=
  array_params = {}
  for name, param in sig.parameters.items():
    array_param = _get_array_param(param, hints)
    if array_param is not None:
      array_params[name] = array_param

  if not array_params:
    raise ValueError(
        f'Could not detect any array type hints in {fn.__qualname__} with '
        f'signature {sig}.'
    )

  return _FnSignatureCache(
      sig=sig,
      has_xnp_kwargs='xnp' in sig.parameters,
      array_params=array_params,
  )


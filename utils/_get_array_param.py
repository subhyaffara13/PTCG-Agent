
def _get_array_param(
    param: inspect.Parameter,
    hints: dict[str, _TypeForm],
) -> Optional[_ArrayParam]:
  """Parse the type & hint of the array."""
  name = param.name
  if name not in hints:  # Not an array param
    return None

  hint = hints[name]

  def make_err(msg: str) -> Exception:
    return NotImplementedError(
        f'`enp.check_and_normalize_arrays` does not support {msg}. Please open '
        f'an issue if you need this feature. For `{name}: {hint}`'
    )

  leaf_types = type_parsing.get_leaf_types(hint)
  is_optional = None in leaf_types
  # Filter Optional
  leaf_types = [t for t in leaf_types if t is not None]

  # Currently, only Optional[Array] or Array supported
  are_array = [isinstance(l, array_typing.ArrayAliasMeta) for l in leaf_types]
  count_array = are_array.count(True)
  count_non_array = are_array.count(False)

  if count_array and count_non_array:
    raise make_err('Union of array and non-array')
  if count_array > 1:
    raise make_err('Union of arrays')
  if count_non_array:
    return None  # Not an array param

  (array_type,) = leaf_types

  if param.kind in {
      inspect.Parameter.VAR_POSITIONAL,
      inspect.Parameter.VAR_KEYWORD,
  }:
    raise make_err('*args, **kwargs')

  return _ArrayParam(
      is_optional=is_optional,
      type=array_type,
      name=name,
  )


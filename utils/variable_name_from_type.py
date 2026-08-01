
def variable_name_from_type(
  typ: tp.Type[Variable[tp.Any]], /, *, allow_register: bool = False
) -> str:
  """Given an NNX Variable type, get its Linen-style collection name.

  Should output the exact inversed result of `variable_type_from_name()`."""
  for name, t in VariableTypeCache.items():
    if typ == t:
      return name

  if not allow_register:
    raise ValueError(
      f'Type {typ} is not registered in the registry. '
      'To register a new type, use register_variable_name() '
      'or set allow_register=True.'
    )
  name = typ.__name__
  if name in VariableTypeCache:
    raise ValueError(
      'Name {name} is already registered in the registry as {VariableTypeCache[name]}. '
      'It cannot be linked with this type {typ}.'
    )
  register_variable_name(name, typ)
  return name


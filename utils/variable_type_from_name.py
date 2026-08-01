
def variable_type_from_name(
  name: str,
  /,
  *,
  base: type[Variable[tp.Any]] = Variable,
  allow_register: bool = False,
) -> tp.Type[Variable[tp.Any]]:
  """Given a Linen-style collection name, get or create its NNX Variable class."""
  if name not in VariableTypeCache:
    if not allow_register:
      raise ValueError(
        f'Name {name} is not registered in the registry. '
        'To register a new name, use register_variable_name() '
        'or set allow_register=True.'
      )
    VariableTypeCache[name] = type(name, (base,), {})
  return VariableTypeCache[name]


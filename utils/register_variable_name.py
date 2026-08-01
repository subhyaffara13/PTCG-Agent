
def register_variable_name(
  name: str,
  typ: type[Variable[tp.Any]],
  *,
  overwrite: bool = False,
) -> type[Variable[tp.Any]]: ...


def register_variable_name(
  name: str,
  *,
  overwrite: bool = False,
) -> tp.Callable[[type[Variable[tp.Any]]], type[Variable[tp.Any]]]: ...


def register_variable_name(
  name: str,
  typ: type[Variable[A]] | Missing = MISSING,
  *,
  overwrite=False,
) -> type[Variable[A]] | tp.Callable[[type[Variable[A]]], type[Variable[A]]]:
  """Register a pair of Linen collection name and its NNX type."""
  if isinstance(typ, Missing):
    return partial(register_variable_name, name, overwrite=overwrite)
  typ = tp.cast(type[Variable[A]], typ)
  if not overwrite and name in VariableTypeCache:
    raise ValueError(
      f'Name {name} already mapped to type {VariableTypeCache[name]}. '
      'To overwrite, call register_variable_name() with `overwrite=True`.'
    )
  VariableTypeCache[name] = typ
  return typ


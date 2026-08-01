
def _variable_unflatten(
  cls: type[Variable[tp.Any]],
  static: tuple[tuple[str, tp.Any], ...],
  children: tuple[tp.Any],
):
  return cls._new(children[0], dict(static))


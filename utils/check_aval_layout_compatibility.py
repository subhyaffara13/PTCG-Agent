
def check_aval_layout_compatibility(
    layouts, flat_avals, names: Sequence[str], what_aval: str):
  for aval, l, name in zip(flat_avals, layouts, names):
    if l is None or isinstance(l, AutoLayoutSingleton):
      continue
    name_str = f' with pytree key path {name}' if name else ''
    try:
      l.check_compatible_aval(aval.shape)
    except ValueError as e:
      raise ValueError(
          f'One of {what_aval}{name_str} is incompatible with its layout '
          f'annotation {l}: {e}')


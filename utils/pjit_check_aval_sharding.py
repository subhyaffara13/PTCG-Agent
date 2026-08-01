
def pjit_check_aval_sharding(
    shardings, flat_avals, names: Sequence[str],
    what_aval: str, allow_uneven_sharding: bool):
  for aval, s, name in zip(flat_avals, shardings, names):
    if isinstance(s, UnspecifiedValue):
      continue
    name_str = f' with pytree key path {name}' if name else ''
    shape = aval.shape
    try:
      s.check_compatible_aval(shape)
    except ValueError as e:
      raise ValueError(
          f'One of {what_aval}{name_str} is incompatible with its sharding '
          f'annotation {s}: {e}')

    if not allow_uneven_sharding:
      s.shard_shape(aval.shape)  # will check for divisibility


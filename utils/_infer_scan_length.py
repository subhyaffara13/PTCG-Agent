
def _infer_scan_length(
    xs_flat: list[Any], xs_avals: list[AbstractValue],
    length: Any | None) -> int:

  # TODO(dougalm): put this in some sort of `scannable` typeclass
  from jax._src.hijax import HiType
  if any(isinstance(a, HiType) for a in xs_avals):
    if length is None:
      raise ValueError("must provide `length` to `scan`")
    else:
      return length

  try:
    lengths: list[int] = [x.shape[0] for x in xs_flat]
  except AttributeError as err:
    msg = "scan got value with no leading axis to scan over: {}."
    raise ValueError(
      msg.format(', '.join(str(x) for x in xs_flat
                           if not hasattr(x, 'shape')))) from err

  xs_shaped_avals = lax_utils.ensure_shaped(*xs_avals)
  if not all(a.sharding.spec.partitions[0] is None for a in xs_shaped_avals):
    raise ValueError('0th dimension of all xs should be replicated. Got '
                     f'{", ".join(str(a.sharding.spec) for a in xs_shaped_avals)}')

  if length is not None:
    try:
      length = int(length)
    except core.ConcretizationTypeError:
      msg = ('The `length` argument to `scan` expects a concrete `int` value.'
             ' For scan-like iteration with a dynamic length, use `while_loop`'
             ' or `fori_loop`.')
      raise core.ConcretizationTypeError(length, msg) from None
    else:
      if not all(length == l for l in lengths):
        msg = ("scan got `length` argument of {} which disagrees with "
              "leading axis sizes {}.")
        raise ValueError(msg.format(length, [x.shape[0] for x in xs_flat]))
      return length
  else:
    unique_lengths = set(lengths)
    if len(unique_lengths) > 1:
      msg = "scan got values with different leading axis sizes: {}."
      raise ValueError(msg.format(', '.join(str(x.shape[0]) for x in xs_flat)))
    elif len(unique_lengths) == 0:
      msg = "scan got no values to scan over and `length` not provided."
      raise ValueError(msg)
    else:
      return list(unique_lengths)[0]


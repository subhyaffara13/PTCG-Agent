
def _mapped_axis_spec(args_flat, in_axes_flat):
  def _get_spec(arg, i):
    try:
      # Duck type arrays like BCOO arrays can be passed to vmap.
      return shaped_abstractify(arg).sharding.spec[i]
    except (IndexError, TypeError, AttributeError):
      return None

  out_spec = None
  non_none_count = 0
  for arg, i in zip(args_flat, in_axes_flat):
    if i is not None:
      spec = _get_spec(arg, i)
      if non_none_count != 0 and out_spec != spec:
        raise ValueError(
            "Mapped away dimension of inputs passed to vmap should be sharded"
            f" the same. Got inconsistent axis specs: {out_spec} vs {spec}")
      out_spec = spec
      non_none_count += 1
  if out_spec is not None and not isinstance(out_spec, tuple):
    out_spec = (out_spec,)
  return out_spec


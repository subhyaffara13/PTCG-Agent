
def _check_ema_unmapped_args(ema, args_flat, in_axes_flat):
  if ema is None:
    return
  for a, i in zip(args_flat, in_axes_flat):
    if i is None:
      aval = core.typeof(a)
      spec = set(sharding_impls.flatten_spec(aval.sharding.spec))
      if any(e in spec for e in ema):
        raise ValueError(
            "Unmapped values passed to vmap cannot be sharded along the mesh"
            f" axis you are vmapping over. Got type: {aval.str_short(True)},"
            f" in_axes: {i} and vmapped mesh axis: {ema}")


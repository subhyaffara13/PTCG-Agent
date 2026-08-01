
def maybe_auto_axes(f, out_sharding, **hoist_kwargs):
  f_ = partial(f, **hoist_kwargs)
  if out_sharding is None:
    return f_
  else:
    return auto_axes(f_, out_sharding=out_sharding,
                     axes=out_sharding.mesh.explicit_axes)


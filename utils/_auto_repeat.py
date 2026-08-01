
def _auto_repeat(fun, a, repeats, axis, total_repeat_length, out_sharding):
  out_sharding = canonicalize_sharding(out_sharding, 'repeat')
  if total_repeat_length is None:
    return auto_axes(partial(fun, repeats, axis=axis,
                             total_repeat_length=total_repeat_length),
                     out_sharding=out_sharding,
                     axes=out_sharding.mesh.explicit_axes
                     )(a)
  else:
    return auto_axes(
        partial(fun, axis=axis, total_repeat_length=total_repeat_length),
        out_sharding=out_sharding,
        axes=out_sharding.mesh.explicit_axes
        )(repeats, a)


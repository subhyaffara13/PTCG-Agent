
def matchaxis(axis_data, src, dst, x, sum_match=False):
  try:
    _ = core.typeof(x)
  except TypeError as e:
    raise TypeError(f"Output from batched function {x!r} with type "
                    f"{type(x)} is not a valid JAX type") from e
  if src == dst or dst is infer:
    return x
  elif type(src) == type(dst) == int:
    return moveaxis(x, src, dst)
  elif src is None and type(dst) is int:
    return broadcast(x, axis_data.size, canonicalize_axis(dst, np.ndim(x) + 1),
                     axis_data.explicit_mesh_axis)
  elif src is None and dst is sum_axis:
    return x
  elif dst is None and sum_match or dst is sum_axis:
    return x.sum(src)
  else:
    if (not isinstance(axis_data.name, core._TempAxisName) and
        axis_data.name is not core.no_axis_name):
      raise ValueError(
          f'vmap has mapped output (axis_name={axis_data.name}) but out_axes is'
          f' {dst}')
    else:
      raise SpecMatchError(None, None, None)


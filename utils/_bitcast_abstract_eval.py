
def _bitcast_abstract_eval(x, *, ty):
  shape = list(x.shape)
  src_bitwidth = dtypes.itemsize_bits(x.dtype)
  dst_bitwidth = dtypes.itemsize_bits(ty)
  shape[-2] = shape[-2] * src_bitwidth // dst_bitwidth
  return jax_core.ShapedArray(shape, ty)


def _bitcast_abstract_eval(x, dtype):
  old_bitwidth = dtypes.itemsize_bits(x.dtype)
  new_bitwidth = dtypes.itemsize_bits(dtype)
  if old_bitwidth == new_bitwidth:
    return jax_core.ShapedArray(x.shape, dtype)
  if x.ndim == 0:
    raise ValueError(
        "Cannot bitcast a ()-shaped array to a dtype with a different bitwidth:"
        f" {old_bitwidth=} vs {new_bitwidth=}"
    )
  new_last_dim, rem = divmod(x.shape[-1] * old_bitwidth, new_bitwidth)
  if rem:
    raise ValueError(
        f"Cannot bitcast from {x.dtype} ({old_bitwidth} bits) to"
        f" {dtype} ({new_bitwidth} bits), because {x.shape[-1]=} *"
        f" {old_bitwidth} is not divisible by {new_bitwidth}"
    )
  return jax_core.ShapedArray((*x.shape[:-1], new_last_dim), dtype)


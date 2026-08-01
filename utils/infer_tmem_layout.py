
def infer_tmem_layout(
    shape: tuple[int, ...],
    dtype: jax.typing.DTypeLike,
    *,
    packed: bool,
    collective: bool) -> tcgen05.TMEMLayout:
  """Infers the number of columns used and layout for allocating TMEM Refs."""
  if packed:
    packing = 32 // dtypes.itemsize_bits(dtype)
  else:
    packing = 1
  return tcgen05._infer_tmem_layout(shape, collective=collective, packing=packing)


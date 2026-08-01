
def _make_top_k_harness(name,
                        *,
                        operand=None,
                        shape=(5, 3),
                        dtype=np.float32,
                        k=2):
  if operand is None:
    operand = RandArg(shape, dtype)
  define(
      lax.top_k_p,
      f"{name}_inshape={jtu.format_shape_dtype_string(operand.shape, operand.dtype)}_{k=}",
      lax.top_k, [operand, StaticArg(k)],
      shape=operand.shape,
      dtype=operand.dtype,
      k=k)


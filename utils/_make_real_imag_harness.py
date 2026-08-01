
def _make_real_imag_harness(prim, name, *, shape=(2, 3), dtype=np.float32):
  define(
      prim,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}",
      prim.bind, [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      prim=prim)


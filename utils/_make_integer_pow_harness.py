
def _make_integer_pow_harness(name, *, shape=(20, 30), dtype=np.int32, y=3):
  define(
      "integer_pow",
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{y=}",
      lax.integer_pow,
      [RandArg(shape, dtype), StaticArg(y)],
      shape=shape,
      dtype=dtype,
      y=y)


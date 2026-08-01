
def _make_rev_harness(name, *, shape=(4, 5), dtype=np.float32, dimensions=(0,)):
  define(
      "rev",
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{dimensions=}",
      lax.rev,
      [RandArg(shape, dtype), StaticArg(dimensions)],
      shape=shape,
      dtype=dtype,
      dimensions=dimensions)


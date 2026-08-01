
def _make_squeeze_harness(name,
                          shape=(1, 2),
                          dimensions=(0,),
                          dtype=np.float32):
  define(
      lax.squeeze_p,
      f"{name}_inshape={jtu.format_shape_dtype_string(shape, dtype)}_{dimensions=}",
      lax.squeeze,
      [RandArg(shape, dtype), StaticArg(dimensions)],
      dtype=dtype,
      arg_shape=shape,
      dimensions=dimensions)


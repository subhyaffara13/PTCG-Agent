
def _make_reshape_harness(name,
                          *,
                          shape=(2, 3),
                          new_sizes=(3, 2),
                          dimensions=(0, 1),
                          dtype=np.float32):
  define(
      "reshape",
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_newsizes={new_sizes}_{dimensions=}",
      lax.reshape,
      [RandArg(shape, dtype),
       StaticArg(new_sizes),
       StaticArg(dimensions)],
      shape=shape,
      dtype=dtype,
      new_sizes=new_sizes,
      dimensions=dimensions)


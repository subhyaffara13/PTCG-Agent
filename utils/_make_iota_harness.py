
def _make_iota_harness(name, *, shape=(2, 3), dtype=np.float32, dimension=0):
  define(
      lax.iota_p,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{dimension=}",
      lambda dtype, shape, dim:
      (lax.iota_p.bind(dtype=np.dtype(dtype), shape=shape, dimension=dim,
                       sharding=None)),
      [StaticArg(dtype),
       StaticArg(shape),
       StaticArg(dimension)],
      shape=shape,
      dtype=dtype,
      dimension=dimension,
      sharding=None)


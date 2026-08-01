
def _make_bitcast_convert_type_harness(name,
                                       *,
                                       shape=(2, 3),
                                       dtype=np.float32,
                                       new_dtype=np.float32):
  define(
      "bitcast_convert_type",
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_newdtype={np.dtype(new_dtype).name}",
      lambda x: lax.bitcast_convert_type_p.bind(x,
                                                new_dtype=np.dtype(new_dtype)),
      [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      new_dtype=new_dtype)


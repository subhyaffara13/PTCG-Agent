
def _make_convert_element_type_harness(name,
                                       *,
                                       shape=(100, 100),
                                       dtype=np.float32,
                                       new_dtype=np.float32):
  define(
      "convert_element_type",
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_olddtype={jtu.dtype_str(dtype)}_newdtype={jtu.dtype_str(new_dtype)}",
      lambda arg: (lax.convert_element_type_p.bind(
          arg, new_dtype=np.dtype(new_dtype), weak_type=False, sharding=None)),
      [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      new_dtype=new_dtype)


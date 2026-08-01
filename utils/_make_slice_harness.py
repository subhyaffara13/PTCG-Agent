
def _make_slice_harness(name,
                        shape=(3,),
                        start_indices=(1,),
                        limit_indices=(2,),
                        strides=None,
                        dtype=np.float32):
  define(
      lax.slice_p,
      f"{name}_a={jtu.format_shape_dtype_string(shape, dtype)}_{start_indices=}_{limit_indices=}_{strides=}",
      lax.slice,
      [
          RandArg(shape, dtype),
          StaticArg(start_indices),
          StaticArg(limit_indices),
          StaticArg(strides)
      ],
      dtype=dtype,
      shape=shape,
      start_indices=start_indices,
      limit_indices=limit_indices)


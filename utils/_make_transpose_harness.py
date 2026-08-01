
def _make_transpose_harness(name,
                            *,
                            shape=(2, 3),
                            permutation=(1, 0),
                            dtype=np.float32):
  define(
      lax.transpose_p,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{permutation=}"
      .replace(" ", ""),
      lambda x: lax.transpose_p.bind(x, permutation=permutation),
      [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      permutation=permutation)


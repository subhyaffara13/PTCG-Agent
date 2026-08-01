
def _make_clamp_harness(name,
                        *,
                        min_shape=(),
                        operand_shape=(2, 3),
                        max_shape=(),
                        dtype=np.float32,
                        min_max=None):
  min_arr, max_arr = (
      min_max if min_max is not None else
      [RandArg(min_shape, dtype),
       RandArg(max_shape, dtype)])
  define(
      lax.clamp_p,
      f"{name}_min={jtu.format_shape_dtype_string(min_arr.shape, min_arr.dtype)}_operand={jtu.format_shape_dtype_string(operand_shape, dtype)}_max={jtu.format_shape_dtype_string(max_arr.shape, max_arr.dtype)}",
      lax.clamp, [min_arr, RandArg(operand_shape, dtype), max_arr],
      min_shape=min_arr.shape,
      operand_shape=operand_shape,
      max_shape=max_arr.shape,
      dtype=dtype,
      jax_unimplemented=[
          Limitation(
              "unimplemented",
              dtypes=[np.bool_, np.complex64, np.complex128])],
  )



def _check_shape_dtype(shape_dtype):
  dt = np.dtype(shape_dtype.dtype)
  if dtypes.canonicalize_dtype(dt) != dt:
    raise ValueError(
        "result_shape_dtypes cannot specify 64-bit types when `jax_enable_x64` is disabled")


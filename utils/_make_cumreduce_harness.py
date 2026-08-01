
def _make_cumreduce_harness(name,
                            *,
                            f_jax=lax_control_flow.cummin,
                            shape=(8, 9),
                            dtype=np.float32,
                            axis=0,
                            reverse=False):
  limitations = []
  define(
      f_jax.__name__,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{axis=}_{reverse=}",
      f_jax, [RandArg(shape, dtype),
              StaticArg(axis),
              StaticArg(reverse)],
      jax_unimplemented=limitations,
      f_jax=f_jax,
      shape=shape,
      dtype=dtype,
      axis=axis,
      reverse=reverse,
      associative_scan_reductions=False
  )
  define(
      f_jax.__name__,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_associative_scan_reductions_{axis=}_{reverse=}",
      f_jax, [RandArg(shape, dtype),
              StaticArg(axis),
              StaticArg(reverse)],
      jax_unimplemented=limitations,
      f_jax=f_jax,
      shape=shape,
      dtype=dtype,
      axis=axis,
      reverse=reverse,
      associative_scan_reductions=True
  )



def _batch_jaxpr_outer(f, axis_data, in_dims, *in_vals):
  in_dims = in_dims() if callable(in_dims) else in_dims
  in_dims = [canonicalize_axis(ax, np.ndim(x)) if isinstance(ax, int)
             else ax for x, ax in unsafe_zip(in_vals, in_dims)]  # pyrefly: ignore[bad-argument-type]  # pyrefly#2385
  tag = TraceTag()
  return f(tag, in_dims, *in_vals)


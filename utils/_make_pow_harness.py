
def _make_pow_harness(name,
                      *,
                      shapes=((20, 30), (20, 30)),
                      dtype=np.float32,
                      lhs=None,
                      rhs=None):
  lhs = RandArg(shapes[0], dtype) if lhs is None else lhs
  rhs = RandArg(shapes[1], dtype) if rhs is None else rhs
  define(
      "pow",
      f"{name}_lhs={jtu.format_shape_dtype_string(lhs.shape, dtype)}_rhs={jtu.format_shape_dtype_string(rhs.shape, dtype)}",
      lax.pow, [lhs, rhs],
      lhs=lhs,
      rhs=rhs,
      dtype=dtype)


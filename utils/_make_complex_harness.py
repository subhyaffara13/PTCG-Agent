
def _make_complex_harness(name, *, shapes=((3, 4), (3, 4)), dtype=np.float32):
  define(
      lax.complex_p,
      f"{name}_lhs={jtu.format_shape_dtype_string(shapes[0], dtype)}_rhs={jtu.format_shape_dtype_string(shapes[1], dtype)}",
      lax.complex_p.bind,
      [RandArg(shapes[0], dtype),
       RandArg(shapes[1], dtype)],
      shapes=shapes,
      dtype=dtype)


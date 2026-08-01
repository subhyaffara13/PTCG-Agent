
def _make_add_any_harness(name, *, shapes=((2,), (2,)), dtype=np.float32):
  define(
      ad_util.add_any_p,
      f"{name}_lhs={jtu.format_shape_dtype_string(shapes[0], dtype)}_rhs={jtu.format_shape_dtype_string(shapes[1], dtype)}",
      ad_util.add_jaxvals_p.bind,
      list(map(lambda s: RandArg(s, dtype), shapes)),
      dtype=dtype,
      shapes=shapes)


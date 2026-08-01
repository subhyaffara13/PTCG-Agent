
def _make_conj_harness(name, *, shape=(3, 4), dtype=np.float32, **kwargs):
  define(
      lax.conj_p,
      f"{name}_operand={jtu.format_shape_dtype_string(shape, dtype)}_{kwargs=}"
      .replace(" ", ""),
      lambda x: lax.conj_p.bind(x, **kwargs), [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      **kwargs)



def _make_concatenate_harness(name,
                              *,
                              shapes=[(2, 3), (2, 3)],
                              dimension=0,
                              dtype=np.float32):
  shapes_str = "_".join(jtu.format_shape_dtype_string(s, dtype) for s in shapes)
  define(
      lax.concatenate_p,
      f"{name}_shapes={shapes_str}_{dimension=}",
      lambda *args: lax.concatenate_p.bind(*args, dimension=dimension),
      [RandArg(shape, dtype) for shape in shapes],
      shapes=shapes,
      dtype=dtype,
      dimension=dimension)


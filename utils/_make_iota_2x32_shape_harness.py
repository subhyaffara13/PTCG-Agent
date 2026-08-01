
def _make_iota_2x32_shape_harness(shape):
  shapestr = ','.join(str(dim) for dim in shape)
  define(
      prng.iota_2x32_shape_p,
      f"shape=({shapestr})",
      lambda shape: prng.iota_2x32_shape_p.bind(shape=shape),
      [StaticArg(shape)],
      dtype=np.uint32,
      shape=shape)


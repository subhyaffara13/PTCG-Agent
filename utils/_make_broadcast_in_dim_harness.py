
def _make_broadcast_in_dim_harness(name,
                                   *,
                                   dtype=np.float32,
                                   shape=(2,),
                                   outshape=(2,),
                                   broadcast_dimensions=(0,)):
  define(
      lax.broadcast_in_dim_p,
      f"{name}_shape={jtu.format_shape_dtype_string(shape, dtype)}_{outshape=}_broadcastdimensions={broadcast_dimensions}",
      lambda operand: lax.broadcast_in_dim_p.bind(
          operand, shape=outshape, broadcast_dimensions=broadcast_dimensions,
          sharding=None),
      [RandArg(shape, dtype)],
      shape=shape,
      dtype=dtype,
      outshape=outshape,
      broadcast_dimensions=broadcast_dimensions)


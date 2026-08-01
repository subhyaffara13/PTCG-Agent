
def _broadcast_in_dim_jvp_rule(primals, tangents, *, shape, broadcast_dimensions,
                               sharding):
  operand, = primals
  operand_dot, *_ = tangents
  y = broadcast_in_dim_p.bind(operand, shape=shape,
                              broadcast_dimensions=broadcast_dimensions,
                              sharding=sharding)
  if type(operand_dot) is ad_util.Zero:
    y_dot = ad_util.p2tz(y)
  else:
    y_dot = broadcast_in_dim_p.bind(operand_dot, shape=shape,
                                    broadcast_dimensions=broadcast_dimensions,
                                    sharding=sharding)
  return y, y_dot


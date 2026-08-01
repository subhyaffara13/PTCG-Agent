
def _reshard_jvp_rule(primals, tangents, *, dst_sharding, concrete_mesh):
  (p,), (t,) = primals, tangents
  primal_out = reshard_p.bind(p, dst_sharding=dst_sharding,
                              concrete_mesh=concrete_mesh)
  if type(t) is ad.Zero:
    return primal_out, ad.p2tz(primal_out)
  else:
    tangent_out = reshard_p.bind(t, dst_sharding=dst_sharding,
                                 concrete_mesh=concrete_mesh)
    return primal_out, tangent_out


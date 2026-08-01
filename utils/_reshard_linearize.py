
def _reshard_linearize(is_vjp, nzs, x, *, dst_sharding, concrete_mesh):
  (nz,) = nzs
  primal_out = reshard_p.bind(x, dst_sharding=dst_sharding,
                              concrete_mesh=concrete_mesh)

  def linearized(residuals, tangent):
    assert not residuals
    return (reshard_p.bind(tangent, dst_sharding=dst_sharding,
                           concrete_mesh=concrete_mesh)
            if nz else ad.p2tz(tangent))
  return primal_out, nz, (), linearized


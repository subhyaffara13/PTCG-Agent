
def _core_map_to_lojax(*consts, jaxpr, mesh, **params):
  closed_hi_jaxpr = jax_core.ClosedJaxpr(jaxpr, consts)
  with (
      tracing_grid_env(tuple(mesh.shape.values()), mapped_dims=()),
      jax_core.extend_axis_env_nd(mesh.shape.items()),
  ):
    closed_lo_jaxpr = pe.lower_jaxpr2(closed_hi_jaxpr)
  assert not closed_lo_jaxpr.is_high
  return core_map_p.bind(
      *closed_lo_jaxpr.consts,
      jaxpr=closed_lo_jaxpr.jaxpr,
      mesh=mesh,
      **params,
  )


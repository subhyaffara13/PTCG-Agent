
def _spec_has_trivial_windowing(spec, grid, full_shape):
  if spec is None:
    return True
  if spec.block_shape is None:
    return True
  for bs, fs in jax_util.safe_zip(spec.block_shape, full_shape):
    if bs is None:
      return False
    if isinstance(
        bs,
        (BoundedSlice, Indirect, Squeezed, Element),
    ):
      return False
    if pallas_core.get_block_size(bs) != fs:
      return False
  if spec.index_map is None:
    return True
  nontrivial_dims = {
      i for i, d in enumerate(grid) if not isinstance(d, int) or d != 1
  }
  if not nontrivial_dims:
    return True
  static_dummy_grid = tuple(d if isinstance(d, int) else 2 for d in grid)
  with pallas_core.tracing_grid_env(static_dummy_grid, mapped_dims=()):
    closed_jaxpr = jax.make_jaxpr(spec.index_map)(*[0] * len(grid))
  jaxpr = closed_jaxpr.jaxpr
  # Refs can be mutated while the pipeline is running so we should not assume
  # that they are constant.
  if any(isinstance(v.aval, state.AbstractRef) for v in jaxpr.constvars):
    return False
  nontrivial_invar_ids = {id(jaxpr.invars[i]) for i in nontrivial_dims}
  for v in jaxpr.outvars:
    if id(v) in nontrivial_invar_ids:
      return False
  for eqn in jaxpr.eqns:
    for v in eqn.invars:
      if id(v) in nontrivial_invar_ids:
        return False
  return True


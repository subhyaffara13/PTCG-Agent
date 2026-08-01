
def _select_hlo_lowering_opaque(ctx, which, *cases):
  avals_in = ctx.avals_in
  aval_out, = ctx.avals_out
  assert all((aval_case.shape, aval_case.dtype) == (aval_out.shape, aval_out.dtype)
             for aval_case in avals_in[1:])
  assert all(
      aval_case == aval_out for aval_case in avals_in[1:]
      if not aval_case.sharding.mesh.empty and not aval_out.sharding.mesh.empty)
  select_lower = _select_hlo_lowering

  physical_aval_out = core.physical_aval(aval_out)
  physical_avals_cases = [physical_aval_out] * (len(avals_in) - 1)
  aval_which = avals_in[0]
  aval_which_bcast = physical_aval_out.update(dtype=aval_which.dtype)
  assert aval_which_bcast.shape[:aval_which.ndim] == aval_which.shape

  bcast_dims = list(range(aval_which.ndim))
  which_bcast = mlir.broadcast_in_dim(
      ctx, which, aval_which_bcast, broadcast_dimensions=bcast_dims)

  return mlir.delegate_lowering(
      ctx, select_lower, which_bcast, *cases,
      avals_in=[aval_which_bcast, *physical_avals_cases],
      avals_out=[physical_aval_out])[0]


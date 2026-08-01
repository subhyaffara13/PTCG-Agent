
def call_shape_dtype_sharding_rule(
    prim, shape_rule, dtype_rule, sharding_rule, ur_rule, multi_out, *avals,
    **kwargs):
  out_shapes = shape_rule(*avals, **kwargs)
  out_dtypes = dtype_rule(*avals, **kwargs)
  num_out = len(out_shapes) if multi_out else None
  try:
    out_shardings = call_sharding_rule(prim, sharding_rule, ur_rule, num_out,
                                       *avals, **kwargs)
  except DuplicateSpecError as e:
    if multi_out:
      raise
    avals_str = ', '.join(i.str_short(short_dtypes=True) for i in avals)
    mesh = mesh_lib.empty_abstract_mesh if e.mesh is None else e.mesh
    out_aval_str = core.str_short_aval(
        out_shapes, out_dtypes, mesh, e.pspec, core.empty_mat,
        core.MemorySpace.Device, short_dtypes=True)
    raise core.ShardingTypeError(
        f'{prim} operation with inputs: {avals_str} produces an illegally'
        f' sharded result: {out_aval_str}') from e
  return out_shapes, out_dtypes, out_shardings


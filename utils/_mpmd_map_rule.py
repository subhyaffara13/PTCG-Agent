
def _mpmd_map_rule(ctx: Context, *args, jaxprs, meshes, external_meshes, **params):
  _assert_no_fusion_types(ctx.avals_in)
  _assert_no_fusion_types(ctx.avals_out)
  all_meshes = meshes + external_meshes
  new_jaxprs = []
  for mesh, jaxpr in zip(meshes, jaxprs):
    with mpmd.mpmd_map_tracing_context(mesh, all_meshes):
      new_jaxprs.append(physicalize_jaxpr(jaxpr))
  return mpmd.mpmd_map_p.bind(
      *args,
      jaxprs=tuple(new_jaxprs),
      meshes=meshes,
      external_meshes=external_meshes,
      **params,
  )


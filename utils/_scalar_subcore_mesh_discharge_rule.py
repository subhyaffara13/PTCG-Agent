
def _scalar_subcore_mesh_discharge_rule(
    in_avals,
    out_avals,
    *args,
    mesh,
    jaxpr,
    compiler_params,
    interpret,
    debug,
    cost_estimate,
    name,
    metadata,
):
  if not isinstance(mesh, ScalarSubcoreMesh):
    raise TypeError(f"Mesh must be a ScalarSubcoreMesh, got {type(mesh)}")
  assert len(mesh.shape) == 1
  if compiler_params is None:
    compiler_params = tpu_core.CompilerParams()
  if compiler_params.dimension_semantics is not None:
    raise ValueError("ScalarSubcoreMesh does not support dimension_semantics=")
  jaxpr, in_avals, out_avals, args, is_scalar_const = tpu_core.pass_scalars_as_refs(
      jaxpr, args, in_avals, out_avals, mesh,
      # TODO(sharadmv): Delete this once we can pass into SMEM directly on
      # SparseCore.
      copy_to_smem=True,
  )
  refs_out, out = pallas_core.default_mesh_discharge_rule(
      in_avals,
      out_avals,
      *args,
      mesh=mesh,
      jaxpr=jaxpr,
      compiler_params=compiler_params,
      interpret=interpret,
      debug=debug,
      cost_estimate=cost_estimate,
      name=name,
      metadata=metadata,
  )
  refs_out = [
      a if not is_scalar else None
      for is_scalar, a in zip(is_scalar_const, refs_out)
  ]
  return refs_out, out


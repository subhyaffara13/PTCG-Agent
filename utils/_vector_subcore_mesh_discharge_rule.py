
def _vector_subcore_mesh_discharge_rule(
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
  if not isinstance(mesh, VectorSubcoreMesh):
    raise TypeError(f"Mesh must be a VectorSubcoreMesh, got {type(mesh)}")
  assert len(mesh.shape) == 2
  if compiler_params is None:
    compiler_params = tpu_core.CompilerParams()
  if compiler_params.dimension_semantics is not None:
    raise ValueError("VectorSubcoreMesh does not support dimension_semantics=")
  return pallas_core.default_mesh_discharge_rule(
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


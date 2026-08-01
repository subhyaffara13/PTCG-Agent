
def _gpu_mesh_discharge_rule(
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
  if not isinstance(mesh, Mesh):
    raise TypeError(f"Mesh must be a `plgpu.Mesh`, got {type(mesh)}")
  if compiler_params and not isinstance(compiler_params, CompilerParams):
    raise TypeError(
        "Compiler params must be a `plgpu.CompilerParams`, got"
        f" {type(compiler_params)}"
    )
  if not compiler_params:
    compiler_params = CompilerParams()
  sa_avals = [a for a in in_avals if isinstance(a, jax_core.ShapedArray)]
  if sa_avals:
    raise NotImplementedError(
        f"Cannot close over values in core_map: {sa_avals}"
    )
  return pallas_core.default_mesh_discharge_rule(
      in_avals,
      out_avals,
      *args,
      jaxpr=jaxpr,
      mesh=mesh,
      compiler_params=compiler_params,
      debug=debug,
      interpret=interpret,
      cost_estimate=cost_estimate,
      name=name,
      metadata=metadata,
  )


from typing import Any

def _tensorcore_mesh_discharge_rule(
    in_avals,
    out_avals,
    *args,
    mesh,
    jaxpr,
    compiler_params: Any | None,
    interpret: Any,
    debug: bool,
    cost_estimate: pallas_core.CostEstimate | None,
    name: str,
    metadata: FrozenDict[str, str] | None,
):
  assert isinstance(mesh, TensorCoreMesh)
  if compiler_params and not isinstance(compiler_params, CompilerParams):
    raise ValueError("compiler_params must be a pltpu.CompilerParams")
  if not compiler_params:
    compiler_params = CompilerParams()
  if len(mesh.shape) > 1:
    raise NotImplementedError("Mesh must be 1D")
  if compiler_params.dimension_semantics is not None:
    raise ValueError("dimension_semantics must be None for TensorCoreMesh")
  num_cores = len(mesh.devices)
  if num_cores > 1:
    # Since each core will have its own VMEM, we currently disallow VMEM inputs
    # and outputs since other ops might not agree on how they are sharded across
    # cores by the (core-mapped) kernel.
    if any(
        pallas_core.get_memory_space_aval(aval) == MemorySpace.VMEM
        for aval in in_avals
    ):
      raise NotImplementedError(
          "TensorCoreMesh does not support VMEM inputs/outputs when there are"
          " >1 cores. Use HBM or ANY instead."
      )
  jaxpr, in_avals, out_avals, args, is_scalar_const = pass_scalars_as_refs(
      jaxpr, args, in_avals, out_avals, mesh
  )
  refs_out, out = pallas_core.default_mesh_discharge_rule(
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
  refs_out = [
      a if not is_scalar else None
      for is_scalar, a in zip(is_scalar_const, refs_out)
  ]
  return refs_out, out


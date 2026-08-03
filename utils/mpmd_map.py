from typing import Any, Callable

def mpmd_map(
    meshes_and_fns: Sequence[tuple[pallas_core.Mesh, Callable[..., None]]],
    /,
    out_types: tree_util.PyTree = (),
    *,
    scratch_types: pallas_core.ScratchShapeTree = (),
    compiler_params: Any | None = None,
    interpret: bool | Any = False,
    debug: bool = False,
    cost_estimate: pallas_core.CostEstimate | None = None,
    name: str | None = None,
    metadata: dict[str, str] | None = None,
) -> Callable[..., _T]:
  interpret = (
      config.pallas_tpu_interpret_mode_context_manager.value or interpret
  )
  return _mpmd_map(
      meshes_and_fns,
      out_types,
      input_output_aliases={},
      scratch_types=scratch_types,
      compiler_params=compiler_params,
      interpret=interpret,
      debug=debug,
      cost_estimate=cost_estimate,
      name=name,
      metadata=metadata,
  )


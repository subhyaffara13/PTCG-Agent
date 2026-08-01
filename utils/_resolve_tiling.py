
def _resolve_tiling(
    mosaic_params: tpu_core.CompilerParams,
    kernel_type: tpu_core.CoreType | None,
) -> tpu_custom_call.Tiling | None:
  if kernel_type is tpu_core.CoreType.TC:
    if mosaic_params.use_tc_tiling_on_sc is None:
      return None
    raise ValueError(
        "use_tc_tiling_on_sc= is not supported for TC kernels"
    )

  return (
      tpu_custom_call.Tiling.COMPACT
      if mosaic_params.use_tc_tiling_on_sc
      or mosaic_params.use_tc_tiling_on_sc is None
      else tpu_custom_call.Tiling.SPARSE_CORE
  )


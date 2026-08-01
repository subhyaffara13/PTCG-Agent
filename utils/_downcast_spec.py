
def _downcast_spec(
    spec: gpu_core.BlockSpec | pallas_core.BlockSpec,
) -> gpu_core.BlockSpec:
  # TODO(slebedev): Find a better place for this.
  if spec.pipeline_mode is not None:
    raise NotImplementedError(
        "pl.BlockSpec with pipeline_mode= is not supported"
    )

  if isinstance(spec, gpu_core.BlockSpec):
    return spec

  return gpu_core.BlockSpec(
      block_shape=spec.block_shape,
      index_map=spec.index_map,
      memory_space=spec.memory_space,
      pipeline_mode=spec.pipeline_mode,
  )


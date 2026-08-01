
def _apply_block_transform(
    block_specs: tuple[pallas_core.BlockSpec, ...],
    block_index_transform: BlockIndexTransform | NoBlockIndexTransform,
) -> pallas_core.BlockSpec | pallas_core.NoBlockSpec:

  def make_new_idx_map(block_index_transform):
    if block_index_transform.block_shape is None:
      return None

    def new_idx_map(*args):
      block_indices = tuple(
          None
          if block_spec is pallas_core.no_block_spec
          else block_spec.index_map(*args)
          for block_spec in block_specs
      )
      return block_index_transform.block_index_transform(*block_indices)

    return new_idx_map

  if isinstance(block_index_transform, NoBlockIndexTransform):
    return pallas_core.no_block_spec
  else:
    return pallas_core.BlockSpec(
        block_shape=block_index_transform.block_shape,
        index_map=make_new_idx_map(block_index_transform),
        memory_space=block_index_transform.memory_space,
        pipeline_mode=block_index_transform.pipeline_mode,
    )


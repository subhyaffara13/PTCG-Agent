
def _wrap_block_spec_scalar_prefetch(
    block_spec: pallas_core.BlockSpec,
    num_grid_args: int,
) -> pallas_core.BlockSpec:
  if block_spec is pallas_core.no_block_spec or block_spec.index_map is None:
    return block_spec

  def new_index_map(*args_and_scalar_prefetch):
    args, scalar_prefetch = util.split_list(
        args_and_scalar_prefetch,
        [num_grid_args],
    )
    with _sp_context(*scalar_prefetch):
      return block_spec.index_map(*args)

  return block_spec.replace(index_map=new_index_map)


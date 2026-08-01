
def _block_spec_from_block_mapping(
    bm: pallas_core.BlockMapping,
    which_parallel: Sequence[bool],
) -> pallas_core.BlockSpec:
  eval_index_map = functools.partial(
      jax.core.eval_jaxpr,
      bm.index_map_jaxpr.jaxpr,
      bm.index_map_jaxpr.consts,
  )

  def index_map(*indices):
    # Inject the parallel indices into the sequential ones coming from
    # `emit_pipeline`.
    new_indices = util.merge_lists(
        which_parallel,
        indices,
        [
            primitives.program_id(axis - 1)
            for axis, is_parallel in zip(
                itertools.accumulate(which_parallel), which_parallel
            )
            if is_parallel
        ],
    )
    return eval_index_map(*new_indices)

  return gpu_core.BlockSpec(
      bm.block_shape,
      index_map,
      memory_space=bm.transformed_block_aval.memory_space,
      transforms=bm.transforms,
  )


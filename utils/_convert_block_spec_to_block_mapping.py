
def _convert_block_spec_to_block_mapping(
    block_spec: BlockSpec,
    origin: OriginStr,
    array_aval: jax_core.ShapedArray,
    *,
    # Inputs for the index_map
    index_map_avals: Sequence[jax_core.AbstractValue],
    index_map_tree: tree_util.PyTreeDef,
    grid: GridMappingGrid,
    vmapped_dims: tuple[int, ...],
    allow_captured_consts: bool,
    debug: bool = False,
) -> BlockMapping:
  if block_spec is no_block_spec:
    block_spec = BlockSpec(None, None)
  return block_spec.to_block_mapping(
      origin,
      array_aval,
      index_map_avals=index_map_avals,
      index_map_tree=index_map_tree,
      grid=grid,
      vmapped_dims=vmapped_dims,
      allow_captured_consts=allow_captured_consts,
      debug=debug,
  )


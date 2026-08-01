
def _init_block_transforms(
    block_specs: tuple[pallas_core.BlockSpec, ...],
) -> tuple[BlockIndexTransform | NoBlockIndexTransform, ...]:
  out = []

  # handle trivially identical output block specs as equivalent for
  # block index transform comparisons
  def compare(x, y):
    if x is pallas_core.no_block_spec or y is pallas_core.no_block_spec:
      return x is y
    return (_block_shapes_equal(x.block_shape, y.block_shape) and
            x.index_map is y.index_map)

  equivalent_bs_argnums = []
  for i, bs in enumerate(block_specs):
    for j, equiv_idx in enumerate(equivalent_bs_argnums):
      if compare(bs, block_specs[equiv_idx]):
        equivalent_bs_argnums.append(equiv_idx)
        break
    else:
      equivalent_bs_argnums.append(i)

  for i, bs in enumerate(block_specs):
    if bs is pallas_core.no_block_spec:
      out.append(no_block_index_transform)
    else:
      out.append(
          BlockIndexTransform(
              block_shape=bs.block_shape,
              block_index_transform=_select_block_indices(
                  equivalent_bs_argnums[i]
              ),
              pipeline_mode=bs.pipeline_mode,
          )
      )
  return tuple(out)


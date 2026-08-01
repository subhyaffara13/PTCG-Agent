
def _batch_block_mapping(
    grid_mapping: GridMapping,
    axis_size: int,
    aval: jax_core.ShapedArray,
    dim: int | batching.NotMapped,
    block_mapping: BlockMapping,
) -> BlockMapping:
  def _block_map_function(new_idx, *args):
    drop_last_args = args

    indices = jax_core.eval_jaxpr(
        block_mapping.index_map_jaxpr.jaxpr,
        block_mapping.index_map_jaxpr.consts,
        *drop_last_args,
    )
    unflat_indices = tree_util.tree_unflatten(
        block_mapping.index_map_out_tree, indices)
    if not isinstance(unflat_indices, tuple):
      unflat_indices = (unflat_indices,)
    unflat_indices = list(unflat_indices)
    if dim is not None:
      unflat_indices.insert(dim, new_idx)
    return tuple(unflat_indices)
  idx_avals = [pallas_core.index_map_grid_aval, *block_mapping.index_map_jaxpr.in_avals]

  block_mapping_flat_fn, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(_block_map_function,
                   debug_info=block_mapping.index_map_jaxpr.jaxpr.debug_info.with_unknown_names()),
      tree_util.tree_structure(idx_avals))
  with grid_mapping.trace_env():
    block_mapping_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
        block_mapping_flat_fn,
        idx_avals)
  new_index_map_out_tree = out_tree_thunk()
  shape = block_mapping.block_shape
  if dim is None:
    new_block_shape = shape
    new_array_aval = block_mapping.array_aval
  else:

    new_block_shape = tuple_insert(shape, dim, pallas_core.squeezed)

    array_shape = block_mapping.array_aval.shape

    array_shape = tuple_insert(array_shape, dim, axis_size)

    new_array_aval = jax_core.ShapedArray(
        array_shape, block_mapping.array_aval.dtype
    )

  jaxpr = jax_core.ClosedJaxpr(block_mapping_jaxpr, consts)
  return block_mapping.replace(block_shape=new_block_shape,
                               array_aval=new_array_aval,
                               index_map_jaxpr=jaxpr,
                               index_map_out_tree=new_index_map_out_tree)


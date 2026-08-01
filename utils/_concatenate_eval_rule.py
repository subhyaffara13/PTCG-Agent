
def _concatenate_eval_rule(ctx: KernelEvalContext, *args, dimension):
  # We now handle the case where each of the concatenated array dimensions
  # divides the block size.
  block_spec = ctx.out_block_specs[0]
  block_shape = block_spec.block_shape
  is_element_block = [isinstance(bd, pallas_core.Element) for bd in block_shape]
  if any(is_element_block):
    raise NotImplementedError(
        'Concatenation with Element indexing is not yet supported.'
    )
  block_dim = block_shape[dimension]
  if block_dim is None:
    block_dim = 1

  if block_dim == sum(aval.shape[dimension] for aval in ctx.avals_in):
    # Handle special case if the block contains all of the concatenated
    # array.
    return jax.lax.concatenate(args, dimension=dimension)

  num_blocks = []
  for aval in ctx.avals_in:
    assert isinstance(aval, core.ShapedArray)
    if aval.shape[dimension] % block_dim != 0:
      raise ValueError(
          f'Shape along concat dimension {dimension} must be divisible by the'
          f' block shape {block_shape[dimension]} for all children. Got shape'
          f' {aval.shape}.'
      )
    num_blocks.append(aval.shape[dimension] // block_dim)
  ends = np.cumsum(num_blocks).astype(np.int32)
  starts = np.concatenate(([0], ends[:-1])).astype(np.int32)

  block_indices = ctx.get_out_block_indices()[0]
  block_idx = block_indices[dimension]
  valid_index = 0
  for i in range(len(ctx.avals_in)):
    start, end = starts[i], ends[i]
    is_valid = (start <= block_idx) & (block_idx < end)
    valid_index = jax.lax.select(is_valid, i, valid_index)
  out_dtype = args[0].dtype
  args = [a.astype(jnp.float32) if a.dtype == jnp.bfloat16 else a for a in args]
  valid_block = jax.lax.select_n(valid_index, *args)
  return valid_block.astype(out_dtype)


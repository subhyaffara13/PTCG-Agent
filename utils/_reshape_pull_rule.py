
def _reshape_pull_rule(
    ctx: PullRuleContext,
    block_transform: BlockIndexTransform,
    *,
    dimensions: tuple[int, ...] | None,
    new_sizes: tuple[int, ...],
    sharding: jax.sharding.Sharding,
):
  del sharding, new_sizes
  if dimensions is not None:
    raise NotImplementedError('reshape with None dimensions not supported yet')
  aval_in = ctx.avals_in[0]
  assert isinstance(aval_in, core.ShapedArray)
  aval_out = ctx.avals_out[0]
  assert isinstance(aval_out, core.ShapedArray)

  block_shape = block_transform.block_shape
  shape_in = aval_in.shape
  shape_out = aval_out.shape
  assert np.prod(shape_in) == np.prod(shape_out)

  # Handle merged dims; i.e. (..., m, n, ...) -> (..., m * n, ...).
  i = 0
  j = 0
  merged_dims = []

  while i < len(shape_in) and j < len(shape_out):
    merged = []
    while not merged or np.prod(merged) < shape_out[j]:
      merged.append(shape_in[i])
      i += 1

    if np.prod(merged) > shape_out[j]:
      break  # Dimension has been split (or something more complex).

    merged_dims.append(merged)
    j += 1

  if (i == len(shape_in)) and np.prod(shape_out[j:]) == 1:
    new_block_shape = []
    new_grids = []

    for d, bd, merged in zip(shape_out, block_shape, merged_dims):  # pyrefly#2385
      bs = pallas_core.get_block_size(bd)

      if len(merged) == 1:
        new_grids.append((merged[0] // bs,))
        new_block_shape.append(bd if bd is not None else 1)
        continue

      if not isinstance(bd, (int, pallas_core.Blocked)):
        raise NotImplementedError('reshape merge must use `Blocked` block size')

      num_blocks = pallas_utils.cdiv(d, bs)
      new_block_dims = []
      for md in reversed(merged):
        if bs % md == 0:
          new_block_dims.append(md)
          bs //= md
        elif md % bs == 0:
          new_block_dims.append(bs)
          bs = 1
        else:
          raise NotImplementedError('unsupported reshape merge')

      new_block_dims.reverse()
      new_block_shape.extend(new_block_dims)
      new_grid = [
          np.int32(md // pallas_core.get_block_size(bd))
          for md, bd in zip(merged, new_block_dims)
      ]
      new_grids.append(tuple(new_grid))

      if np.prod(new_grid) != num_blocks:
        raise NotImplementedError('reshape merge must maintain grid size')

    def new_block_index_transform(*idxs):
      # NOTE: The `zip` will drop indices for any trailing `1` dims.
      idxs = (
          jnp.unravel_index(idx, new_grid) if len(new_grid) > 1 else (idx,)
          for idx, new_grid in zip(
              block_transform.block_index_transform(*idxs), new_grids)
      )
      return sum(idxs, ())

    return [block_transform.replace(
            block_shape=tuple(new_block_shape),
                block_index_transform=new_block_index_transform,)]

  # Handle the case where we reshape from (..., n * l) -> (..., n, l)
  if _pattern_match_lanes_to_sublanes_reshape(aval_in, aval_out):
    if not isinstance(block_shape[-1], (int, pallas_core.Blocked)):
      raise NotImplementedError(
          f'reshape must use Blocked block size on lanes: {block_shape}'
      )
    if not isinstance(block_shape[-2], (int, pallas_core.Blocked)):
      raise NotImplementedError(
          f'reshape must use Blocked block size on sublanes: {block_shape}'
      )
    last_dim = aval_out.shape[-1]
    block_sublane_dim, block_lane_dim = (
        _block_size(block_shape[-2]),
        _block_size(block_shape[-1]),
    )
    total_block_size = block_sublane_dim * block_lane_dim
    if total_block_size % 128 != 0:
      raise NotImplementedError(
          'reshape with non-128 aligned block size on lanes not supported yet'
      )
    if block_lane_dim != last_dim:
      raise NotImplementedError(
          'reshape with non-matching block size on lanes not supported yet:'
          f' {block_shape}'
      )
    new_block_shape = (*block_shape[:-2], total_block_size)

    def new_block_index_transform(*idxs):
      *idx, second_to_last, last = block_transform.block_index_transform(*idxs)
      # last should always be 0
      if not isinstance(last, int) and last != 0:
        raise NotImplementedError(
            'Must select entire block on last dimension for reshape'
        )
      return *idx, second_to_last

    return [block_transform.replace(
                block_shape=new_block_shape,
                block_index_transform=new_block_index_transform,)]

  raise NotImplementedError(f'reshape not supported yet: {aval_in}, {aval_out}')


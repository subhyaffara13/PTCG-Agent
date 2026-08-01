
def fetch_with_lookahead(buffered_ref, src_ref,
                         grid,
                         grid_offsets,
                         predicate: jax.Array | bool = True,
                         max_num_fetches: int | None = None,
                         update_slots: bool = True):
  """Fetch future blocks using unbounded lookahead.

  Args:
    buffered_ref: the BufferedRef to fetch for.
    src_ref: the source Ref.
    grid: the grid bounds.
    grid_offsets: the grid offsets (used for megacore).
    predicate: a boolean predicate for whether to perform the fetch.
    max_num_fetches: the maximum number of fetches to perform. If None,
      this will continually fetch until all copy_in slots are full.
    update_slots: whether to update the register slot indices.
  """
  assert buffered_ref.use_lookahead
  add_offset = lambda x: tuple(
      i + j for i, j in zip(x, grid_offsets, strict=True))
  index_inbound = lambda x: _tuple_lt(x, grid)
  increment_indices = lambda x: _next_index(x, grid, allow_overflow=True)
  def as_uint32(x):
    if isinstance(x, bool):
      return jnp.uint32(x)
    else:
      return x.astype(jnp.uint32)

  fetch_limit = buffered_ref.cumulative_wait_in + buffered_ref.buffer_count
  if max_num_fetches is not None:
    fetch_once_limit = buffered_ref.cumulative_copy_in + max_num_fetches
    # We would like to write jnp.minimum(fetch_limit, fetch_once_limit)
    # but this does not compile in Mosaic.
    fetch_limit = lax.select(fetch_limit < fetch_once_limit,
                             fetch_limit, fetch_once_limit)

  def _loop_cond(carry):
    _, next_indices, cumulative_copy_in = carry
    # Don't fetch more blocks than we have buffers.
    within_limit = cumulative_copy_in < fetch_limit
    # Don't fetch past the end of the grid.
    in_bounds = index_inbound(next_indices)
    return predicate & within_limit & in_bounds

  def _loop_body(carry):
    current_indices, next_indices, cumulative_copy_in = carry
    cur_indices_offset = add_offset(current_indices)
    next_indices_offset = add_offset(next_indices)
    block_indices = buffered_ref.compute_index(*cur_indices_offset)
    next_block_indices = buffered_ref.compute_index(*next_indices_offset)
    will_change = _tuples_differ(block_indices, next_block_indices)
    pred = will_change
    bref = buffered_ref.with_slot_index(copy_in_slot=cumulative_copy_in)
    @when(pred)
    def _start():
      bref.copy_in(src_ref, next_indices_offset)
    next_copy_in = cumulative_copy_in + as_uint32(pred)
    next_next_indices = increment_indices(next_indices)
    return next_indices, next_next_indices, next_copy_in
  current_indices = buffered_ref.next_fetch_indices
  next_fetch = increment_indices(current_indices)
  final_indices, _, final_copy_in_slot = lax.while_loop(
      _loop_cond, _loop_body,
      (current_indices, next_fetch, buffered_ref.cumulative_copy_in))

  buffered_ref = buffered_ref.with_next_fetch(final_indices)
  if update_slots:
    buffered_ref = buffered_ref.with_slot_index(copy_in_slot=final_copy_in_slot)
  return buffered_ref, final_copy_in_slot


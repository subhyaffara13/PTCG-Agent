
def _fix_seqlen_offsets(q_seqlen, kv_seqlen, q_offsets, kv_offsets, query, key):
  # fix seqlen and offsets to what cuDNN expects in sequence packing.
  # cuDNN expects seqlen to have shape [S] where S is the total number of segments
  # while the SDPA API accetps seqlen with shape [B, M] where B is the batch and M
  # is the maximum number of segments of one batch. B x M is larger than S and seqlen
  # is filled with -1 for padded regions. Therefore, we need to shift all non negative
  # values to left side to form a correct seqlen. Similar layout is required for
  # offsets tensors.
  # cuDNN expects offsets to have offset for each segment starting from first segment
  # while SDPA API accetps offsets to have offset for each segment starting from
  # current batch, therefore we need to calculate accumulative offset of each segment
  # starting from first segment.
  def _shift_to_left(x, fill_value):
    # shift any non-negative value to left
    # [[1, 3, -1, -1], [2, 3, 4, -1]]
    # -> [[1, 3, 2, 3], [4, -1, -1, -1]]
    x_shape = x.shape
    x = x.flatten()
    size = x.size
    indices = jnp.nonzero(x >= 0, size=size, fill_value=size)[0]
    y = jnp.take(x, indices, fill_value=fill_value)
    return jnp.reshape(y, x_shape)

  def _cu_offset(offsets, max_seq):
    # calculate accumulative offset by batch
    # [[1, 3, 5, 7], [4, 5, -1, -1]], max_seq = 8
    # -> [[1, 3, 5, 7], [12, 13, -1, -1]]
    batch = offsets.shape[0]
    offsets = jnp.where(
        offsets >= 0,
        offsets + (jnp.arange(batch, dtype=offsets.dtype) * max_seq)[..., np.newaxis],
        offsets,
    )
    return offsets

  if get_max_seg_per_batch(q_offsets) > 1:
    B, T, N, H = query.shape
    _, S, _, _ = key.shape

    q_seqlen = _shift_to_left(q_seqlen, 0)
    kv_seqlen = _shift_to_left(kv_seqlen, 0)

    q_offsets = _cu_offset(q_offsets, T)
    kv_offsets = _cu_offset(kv_offsets, S)
    q_offsets = _shift_to_left(q_offsets, B * T)
    kv_offsets = _shift_to_left(kv_offsets, B * S)

    # multiply by stride_per_token to get correct offsets
    # do it here because real stride changes after sharding
    q_offsets = q_offsets * N * H
    kv_offsets = kv_offsets * N * H

  return q_seqlen, kv_seqlen, q_offsets, kv_offsets


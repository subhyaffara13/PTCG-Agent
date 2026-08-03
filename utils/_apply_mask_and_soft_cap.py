import functools

def _apply_mask_and_soft_cap(
    qk: jax.Array,
    mask_value: float,
    should_not_mask,
    mask_ref,
    q_sequence_ref,
    q_segment_ids_ref,
    kv_segment_ids_ref,
    *,
    attn_logits_soft_cap: float | None,
    k_slice: pl.Slice,
    k_offset: int | jax.Array,
    bq: int,
    k_in_lanes=True,
    mask_function=None,
) -> jax.Array:
  assert mask_ref is None or q_sequence_ref is None
  assert (q_sequence_ref is None) == (mask_function is None)

  masks = []
  if mask_ref is not None:
    if k_in_lanes:
      mask = mask_ref[:, k_slice]
    else:
      mask = mask_ref[k_slice, :]

    masks.append(
        jnp.bitwise_or(mask, jnp.broadcast_to(should_not_mask, mask.shape))
    )
  if mask_function is not None:
    assert q_sequence_ref is not None
    # Compute the mask using the given q_sequence indices.
    # KV indices are computed on the fly. This works because we only support Q
    # sequence sharding. If we wanted to compute Q indices too, then we would
    # need to keep into account the current shard along Q sequence.

    if k_in_lanes:
      assert q_sequence_ref.shape == (bq, NUM_LANES)

      k_sequence = k_offset + jax.lax.broadcasted_iota(
          jnp.int32, (bq, k_slice.size), 1
      )

      repeats, rem = divmod(k_slice.size, NUM_LANES)
      assert rem == 0
      q_sequence = jnp.tile(
          q_sequence_ref[...], (1, repeats)
      )  # [bq, k_slice.size]
    else:
      assert q_sequence_ref.shape == (NUM_SUBLANES, bq)

      k_sequence = k_offset + jax.lax.broadcasted_iota(
          jnp.int32, (k_slice.size, bq), 0
      )
      q_sequence = q_sequence_ref[:1, :]  # [1, bq]
      q_sequence = jnp.broadcast_to(q_sequence, (k_slice.size, bq))

    assert q_sequence.shape == k_sequence.shape
    computed_mask = mask_function(q_sequence, k_sequence)
    if computed_mask.dtype != jnp.dtype(jnp.bool_):
      raise ValueError(
          "Mask function must return a boolean-valued array, but got:"
          f" {computed_mask.dtype}"
      )
    masks.append(computed_mask)

  if q_segment_ids_ref is not None:
    if k_in_lanes:
      kv_ids = kv_segment_ids_ref[:1, k_slice]  # [1, k_slice]
      repeats, rem = divmod(kv_ids.shape[1], NUM_LANES)
      if rem:
        raise NotImplementedError(f"block_kv must be a multiple of {NUM_LANES}")
      q_ids = jnp.tile(q_segment_ids_ref[:], (1, repeats))  # [bq, bkv]
    else:
      assert bq == q_segment_ids_ref.shape[-1]
      repeats, rem = divmod(bq, NUM_LANES)
      if rem:
        raise NotImplementedError(f"block_q must be a multiple of {NUM_LANES}")
      kv_ids = jnp.tile(
          kv_segment_ids_ref[k_slice, :], (1, repeats)
      )  # [k_slice, bq]
      q_ids = q_segment_ids_ref[:1, :]  # [1, bq]
    masks.append(q_ids == kv_ids)

  def cap_logits(logits):
    if attn_logits_soft_cap is not None:
      logits = jnp.tanh(qk / attn_logits_soft_cap)
      return logits * attn_logits_soft_cap
    else:
      return logits

  if masks:
    mask = functools.reduce(jnp.logical_and, masks)
    qk = cap_logits(qk)
    qk = jnp.where(mask, qk, mask_value)
  else:
    qk = cap_logits(qk)
  return qk



def segment_mask(
    q_segment_ids: jax.Array,
    kv_segment_ids: jax.Array,
):
  # [B, T, 1] or [T, 1]
  q_segment_ids = jnp.expand_dims(q_segment_ids, axis=-1)
  # [B, 1, S] or [1, S]
  if kv_segment_ids.ndim == 1:
    kv_segment_ids = jnp.expand_dims(kv_segment_ids, axis=0)
  else:
    kv_segment_ids = jnp.expand_dims(kv_segment_ids, axis=1)
  return jnp.equal(q_segment_ids, kv_segment_ids).astype(jnp.bool_)


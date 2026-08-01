
def _attention_reference_custom_bwd(
    mask_value: float,
    save_residuals: bool,
    custom_type: str,
    attn_logits_soft_cap: float | None,
    res,
    do: jax.Array,
) -> tuple[None, jax.Array, jax.Array, jax.Array, None, jax.Array | None]:
  del save_residuals
  mask, q, k, v, segment_ids, sinks, o, logsumexp = res

  uncapped_logits = jnp.einsum(
      "qc,kc->qk", q, k, preferred_element_type=jnp.float32)

  if attn_logits_soft_cap is not None:
    logits = jnp.tanh(uncapped_logits / attn_logits_soft_cap)
    logits = logits * attn_logits_soft_cap
  else:
    logits = uncapped_logits

  if segment_ids is not None:
    mask = jnp.logical_and(
        mask, segment_ids.q[:, None] == segment_ids.kv[None, :]
    )
  logits = jnp.where(mask, logits, mask_value)

  p = jnp.exp(logits - logsumexp[..., None])
  do = do.astype(jnp.float32)
  dv = jnp.einsum("pt,pd->td", p, do).astype(v.dtype)
  dp = jnp.einsum("pd,td->pt", do, v.astype(jnp.float32))

  # These two ways of computing ds are mathematically equivalent. The first
  # involves reducing over the head_dim dimension and the second involves
  # reducing over a sequence dimension. They tend to produce slightly different
  # numerics.
  if custom_type == "flash":
    di = jnp.sum(o.astype(jnp.float32) * do, axis=-1)[..., None]
  else:
    di = jnp.einsum("st,st->s", dp, p)[:, None]
  ds = (dp - di) * p
  if attn_logits_soft_cap is not None:
    normalized = uncapped_logits / attn_logits_soft_cap
    d = jnp.tanh(normalized)
    g = ds * (1 - d)
    ds = g + g * d
  dk = jnp.einsum("sd,st->td", q.astype(jnp.float32), ds).astype(k.dtype)
  dq = jnp.einsum("st,td->sd", ds, k.astype(jnp.float32)).astype(q.dtype)
  dsinks = None
  if sinks is not None:  # the gradient is ``sum(-exp(s) / exp(lse) * o * do)``
    sinks_exp = -jnp.exp(sinks[..., None, None].astype(jnp.float32)
                         - logsumexp[..., None].astype(jnp.float32))
    dsinks = jnp.sum(sinks_exp.astype(o.dtype) * do * o)
  return None, dq, dk, dv, None, dsinks


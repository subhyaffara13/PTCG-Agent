import functools
import math


def gqa(
    q,                # [batch_size, num_q_heads, head_dim]
    k,                # [batch_size, k_seq_len, num_kv_heads, head_dim]
    v,                # [batch_size, k_seq_len, num_kv_heads, head_dim]
    start_idx=None,   # [batch_size]
    kv_seq_len=None,  # [batch_size]
    sm_scale: float | None = None,
    block_h: int = 16,
    block_k: int = 128,
    k_splits: int = 16,
    num_warps: int | None = None,
    num_stages: int = 2,
    grid: tuple[int, ...] | None = None,
    interpret: bool = False,
    debug: bool = False,
    return_residuals: bool = False,
    normalize_output: bool = True,
):
  if not normalize_output and not return_residuals:
    raise NotImplementedError(
        "When normalize_output is False, attention residuals must be returned."
    )
  sm_scale = sm_scale if sm_scale is not None else (1 / math.sqrt(q.shape[-1]))
  batch_size, q_heads, head_dim = q.shape
  _k_seq_len, kv_heads = k.shape[1], k.shape[2]
  assert kv_heads == v.shape[2]
  assert q_heads % kv_heads == 0
  if start_idx is not None:
    assert start_idx.ndim in (0, 1)
    start_idx = jnp.broadcast_to(jnp.asarray(start_idx)[..., None],
                                 (batch_size, kv_heads))
  if kv_seq_len is not None:
    assert kv_seq_len.ndim in (0, 1)
    kv_seq_len = jnp.broadcast_to(jnp.asarray(kv_seq_len)[..., None],
                                  (batch_size, kv_heads))
  q_heads_per_kv_head = q_heads // kv_heads
  q_reshaped = q.reshape(batch_size, kv_heads, q_heads_per_kv_head, head_dim)
  k_transposed = jnp.swapaxes(
      k, 1, 2
  )  # [batch_size, num_kv_heads, k_seq_len, head_dim]
  v_transposed = jnp.swapaxes(
      v, 1, 2
  )  # [batch_size, num_kv_heads, k_seq_len, head_dim]
  inner = functools.partial(
      decode_attn_unbatched,
      sm_scale=sm_scale,
      block_h=block_h,
      block_k=block_k,
      k_splits=k_splits,
      num_warps=num_warps,
      num_stages=num_stages,
      grid=grid,
      interpret=interpret,
      debug=debug,
      return_residuals=return_residuals,
      normalize_output=normalize_output,
  )
  with_kv_heads = jax.vmap(inner)
  outputs = jax.vmap(with_kv_heads)(
      q_reshaped, k_transposed, v_transposed, start_idx, kv_seq_len
  )
  if return_residuals:
    o, (l, m) = outputs
    o = o.reshape(batch_size, q_heads, head_dim)
    l = l.reshape(batch_size, q_heads)
    m = m.reshape(batch_size, q_heads)
    return o, (l, m)
  else:
    o = outputs
    o = o.reshape(batch_size, q_heads, head_dim)
    return o


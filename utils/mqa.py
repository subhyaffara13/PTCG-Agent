import functools
import math


def mqa(
    q,                # [batch_size, num_heads, head_dim]
    k,                # [batch_size, k_seq_len, head_dim]
    v,                # [batch_size, k_seq_len, head_dim]
    start_idx=None,   # [batch_size]
    kv_seq_len=None,  # [batch_size]
    sm_scale: float | None = None,
    block_h: int = 16,
    block_k: int = 256,
    k_splits: int = 16,
    num_warps: int | None = None,
    num_stages: int = 2,
    grid: tuple[int, ...] | None = None,
    interpret: bool = False,
    debug: bool = False,
    return_residuals: bool = False,
    normalize_output: bool = True,
):
  sm_scale = sm_scale if sm_scale is not None else (1 / math.sqrt(q.shape[-1]))
  bs = q.shape[0]
  if start_idx is not None:
    start_idx = jnp.broadcast_to(start_idx, (bs,))
  if kv_seq_len is not None:
    kv_seq_len = jnp.broadcast_to(kv_seq_len, (bs,))
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
  return jax.vmap(inner)(q, k, v, start_idx, kv_seq_len)


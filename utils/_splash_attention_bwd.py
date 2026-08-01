
def _splash_attention_bwd(
    save_residuals: bool,
    mask_value: float,
    is_mqa: bool,
    block_sizes: BlockSizes,
    residual_checkpoint_name: str | None,
    mask_function: MaskFunctionType | None,
    attn_logits_soft_cap: float | None,
    interpret: bool,
    res: SplashResidualsType,
    do: jax.Array,
) -> tuple[
    mask_info_lib.MaskInfo | None,  # fwd_mask_info
    mask_info_lib.MaskInfo | None,  # dq_mask_info
    mask_info_lib.MaskInfo | None,  # dvk_mask_info
    jax.Array,  # q
    jax.Array,  # k
    jax.Array,  # v
    SegmentIds | None,  # segmend_ids
    jax.Array | None,  # sinks
]:
  del save_residuals, residual_checkpoint_name
  if not block_sizes.has_backward_blocks:
    raise ValueError("Need to specify backward blocks.")
  bq_dq, bkv_dq = block_sizes.block_q_dq, block_sizes.block_kv_dq
  bq_dkv, bkv_dkv_memory, bkv_dkv_compute = (
      block_sizes.block_q_dkv,
      block_sizes.block_kv_dkv,
      block_sizes.block_kv_dkv_compute,
  )
  use_fused_bwd_kernel = block_sizes.use_fused_bwd_kernel
  (
      q,
      k,
      v,
      segment_ids,
      sinks,
      o,
      logsumexp,
      dq_mask_info,
      dkv_mask_info,
  ) = res

  # di: [num_heads, q_seq_len]
  di = jnp.einsum("hsd,hsd->hs", o.astype(jnp.float32), do.astype(jnp.float32))
  assert bq_dkv is not None
  assert bkv_dkv_memory is not None
  assert bkv_dkv_compute is not None
  assert dkv_mask_info is not None
  dq, dk, dv = _splash_attention_bwd_dkv(
      q,
      k,
      v,
      segment_ids,
      sinks,
      logsumexp,
      do,
      di,
      bq=bq_dkv,
      bkv=bkv_dkv_memory,
      bkv_compute=bkv_dkv_compute,
      is_mqa=is_mqa,
      mask_info=dkv_mask_info,
      mask_value=mask_value,
      attn_logits_soft_cap=attn_logits_soft_cap,
      use_fused_bwd_kernel=use_fused_bwd_kernel,
      q_layout=block_sizes.q_layout,
      k_layout=block_sizes.k_layout,
      v_layout=block_sizes.v_layout,
      mask_function=mask_function,
      interpret=interpret,
  )
  if not use_fused_bwd_kernel:
    assert dq is None
    assert bq_dq is not None
    assert bkv_dq is not None
    assert dq_mask_info is not None
    dq = _splash_attention_bwd_dq(
        q,
        k,
        v,
        segment_ids,
        sinks,
        logsumexp,
        do,
        di,
        bq=bq_dq,
        bkv=bkv_dq,
        is_mqa=is_mqa,
        mask_info=dq_mask_info,
        mask_value=mask_value,
        attn_logits_soft_cap=attn_logits_soft_cap,
        q_layout=block_sizes.q_layout,
        k_layout=block_sizes.k_layout,
        v_layout=block_sizes.v_layout,
        mask_function=mask_function,
        interpret=interpret,
    )
  # Match the signature of the fwd function.
  assert dq is not None
  dsinks = None
  if sinks is not None:
    sinks_exp = -jnp.exp(sinks[..., None, None].astype(jnp.float32)
                         - logsumexp[..., None].astype(jnp.float32))
    dsinks = jnp.sum(sinks_exp.astype(o.dtype) * o * do, axis=(-1, -2))
  return (
      None,  # fwd_mask_info
      None,  # dq_mask_info
      None,  # dvk_mak_info
      dq,  # q
      dk,  # k
      dv,  # v
      None,  # segment_ids
      dsinks,  # sinks
  )


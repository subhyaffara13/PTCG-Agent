
def _splash_attention_fwd(
    fwd_mask_info: mask_info_lib.MaskInfo,
    dq_mask_info: mask_info_lib.MaskInfo | None,
    dkv_mask_info: mask_info_lib.MaskInfo | None,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None,
    sinks: jax.Array | None,
    save_residuals: bool,
    mask_value: float,
    is_mqa: bool,
    block_sizes: BlockSizes,
    residual_checkpoint_name: str | None,
    mask_function: MaskFunctionType | None,
    attn_logits_soft_cap: float | None = None,
    interpret: bool = False,
) -> tuple[
    jax.Array,
    SplashResidualsType,
]:
  if save_residuals:
    raise NotImplementedError("Higher-order AD not supported")

  out, (logsumexp,) = _splash_attention_forward(
      fwd_mask_info,
      q,
      k,
      v,
      segment_ids,
      sinks,
      mask_value=mask_value,
      is_mqa=is_mqa,
      block_sizes=block_sizes,
      residual_checkpoint_name=residual_checkpoint_name,
      save_residuals=True,
      mask_function=mask_function,
      attn_logits_soft_cap=attn_logits_soft_cap,
      interpret=interpret,
  )
  return out, (
      q,
      k,
      v,
      segment_ids,
      sinks,
      out,
      logsumexp,
      dq_mask_info,
      dkv_mask_info,
  )


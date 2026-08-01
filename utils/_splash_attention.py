
def _splash_attention(
    fwd_mask_info: mask_info_lib.MaskInfo,
    dq_mask_info: mask_info_lib.MaskInfo | None,
    dkv_mask_info: mask_info_lib.MaskInfo | None,
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    segment_ids: SegmentIds | None = None,
    sinks: jax.Array | None = None,
    *,
    is_mqa: bool,
    block_sizes: BlockSizes | None,
    save_residuals: bool,
    mask_value: float,
    attn_logits_soft_cap: float | None,
    residual_checkpoint_name: str | None,
    mask_function: MaskFunctionType | None,
    interpret: bool,
) -> SplashCustomReturnType:
  """
  For dynamic masks, `partial_mask_blocks` has shape (head_count, q_blocks, kv_blocks, block_q, block_kv).
  This shape allows sharding across both head count and query sequence dimensions.

  Note: The leading dimensions (head_count, q_blocks, kv_blocks) must be
  collapsed into a single dimension before being passed to the kernel.
  """
  def _collapse_partial_mask_blocks(mask_info: mask_info_lib.MaskInfo | None):
    if mask_info is None or mask_info.partial_mask_blocks is None:
      return mask_info

    return mask_info._replace(
        partial_mask_blocks=mask_info.partial_mask_blocks.reshape(
            -1, *mask_info.partial_mask_blocks.shape[-2:]
        )
    )

  fwd_mask_info = _collapse_partial_mask_blocks(fwd_mask_info)
  dq_mask_info = _collapse_partial_mask_blocks(dq_mask_info)
  dkv_mask_info = _collapse_partial_mask_blocks(dkv_mask_info)
  return _splash_attention_custom(
      fwd_mask_info,
      dq_mask_info,
      dkv_mask_info,
      q,
      k,
      v,
      segment_ids,
      sinks,
      mask_value=mask_value,
      is_mqa=is_mqa,
      block_sizes=block_sizes,
      save_residuals=save_residuals,
      attn_logits_soft_cap=attn_logits_soft_cap,
      residual_checkpoint_name=residual_checkpoint_name,
      mask_function=mask_function,
      interpret=interpret,
  )


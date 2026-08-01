
def _make_splash_attention(
    mask: np.ndarray | jax.Array | mask_lib.MultiHeadMask,
    *,
    block_sizes: BlockSizes | None = None,
    is_mqa: bool,
    save_residuals: bool = False,
    mask_value: float = DEFAULT_MASK_VALUE,
    attn_logits_soft_cap: float | None = None,
    downcast_smem_data: bool = True,
    head_shards: int,
    q_seq_shards: int,
    residual_checkpoint_name: str | None = None,
    interpret: bool = False,
):
  if len(mask.shape) != 3:
    raise ValueError(f'Unexpected mask shape: {mask.shape}')

  if isinstance(mask, np.ndarray):
    mask = mask_lib.MultiHeadMask(
        [mask_lib.NumpyMask(head_mask) for head_mask in mask]
    )

  if block_sizes is None:
    block_sizes = BlockSizes.get_default()

  process_mask_fn = (
      mask_info_lib.process_dynamic_mask
      if isinstance(mask, jax.Array)
      else mask_info_lib.process_mask
  )

  process_mask_dvk_fn = (
      mask_info_lib.process_dynamic_mask_dkv
      if isinstance(mask, jax.Array)
      else mask_info_lib.process_mask_dkv
  )

  fwd_mask_info, mask_function_fwd = process_mask_fn(
      mask,
      (block_sizes.block_q, block_sizes.block_kv),
      downcast_smem_data=downcast_smem_data,
      head_shards=head_shards,
      q_seq_shards=q_seq_shards,
  )
  fwd_mask_info = tree_util.tree_map(jnp.array, fwd_mask_info)

  dq_mask_info = None
  dkv_mask_info = None
  if block_sizes.has_backward_blocks:
    if block_sizes.use_fused_bwd_kernel:
      dq_mask_info = None
    else:
      bq_dq, bkv_dq = block_sizes.block_q_dq, block_sizes.block_kv_dq
      dq_mask_info, mask_function_dq = process_mask_fn(
          mask,
          (bq_dq, bkv_dq),
          downcast_smem_data=downcast_smem_data,
          head_shards=head_shards,
          q_seq_shards=q_seq_shards,
      )
      assert (mask_function_fwd is None) == (mask_function_dq is None)
      dq_mask_info = tree_util.tree_map(jnp.array, dq_mask_info)
    bq_dkv, bkv_dkv = block_sizes.block_q_dkv, block_sizes.block_kv_dkv
    dkv_mask_info, mask_function_dkv = process_mask_dvk_fn(
        mask,
        (bq_dkv, bkv_dkv),
        downcast_smem_data=downcast_smem_data,
        head_shards=head_shards,
        q_seq_shards=q_seq_shards,
        shrink_grid=not block_sizes.use_fused_bwd_kernel,
    )
    assert (mask_function_fwd is None) == (mask_function_dkv is None)

    dkv_mask_info = tree_util.tree_map(jnp.array, dkv_mask_info)

  return SplashAttentionKernel(
      fwd_mask_info,
      dq_mask_info,
      dkv_mask_info,
      block_sizes=block_sizes,
      is_mqa=is_mqa,
      save_residuals=save_residuals,
      mask_value=mask_value,
      attn_logits_soft_cap=attn_logits_soft_cap,
      residual_checkpoint_name=residual_checkpoint_name,
      mask_function=mask_function_fwd,
      interpret=interpret,
  )


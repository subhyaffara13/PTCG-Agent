
def _paged_decode_forward(
    module: torch.nn.Module,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    cache: PagedAttentionCache,
    cu_seq_lens_k: torch.Tensor,
    sliding_window: tuple[int, int],
    flash_attn_with_kvcache,
    block_table: torch.Tensor,
    **flash_kwargs,
) -> torch.Tensor:
    """Decode fast path using flash_attn_with_kvcache. Disabled because FA3 has issue with tracing this."""
    # Get layer group index for this layer
    group_idx, layer_idx_in_group = cache.layer_index_to_group_indices[module.layer_idx]
    # KV cache shape: [num_pages, num_kv_heads, head_dim] -> [num_blocks, block_size, num_kv_heads, head_dim]
    k_cache = cache.key_cache[layer_idx_in_group].view(-1, cache.block_size, cache.num_key_value_heads, cache.head_dim)
    v_cache = cache.value_cache[layer_idx_in_group].view(
        -1, cache.block_size, cache.num_key_value_heads, cache.head_dim
    )
    # Reshape Q, K, V from [1, num_*_heads, batch_size, head_dim] to [batch_size, 1, num_*_heads, head_dim]
    q = q.permute(2, 0, 1, 3).contiguous()
    k = k.permute(2, 0, 1, 3).contiguous()
    v = v.permute(2, 0, 1, 3).contiguous()
    # Compute cache_seqlens from cu_seq_lens_k (current cache length BEFORE adding new tokens)
    # cu_seq_lens_k is cumulative, so seqlens[i] = cu_seq_lens_k[i+1] - cu_seq_lens_k[i] - 1 (subtract 1 for the new token)
    batch_size = k.size(0)
    cache_seqlens = (cu_seq_lens_k[1 : batch_size + 1] - cu_seq_lens_k[:batch_size] - 1).to(torch.int32)
    # The arg name for the block table is not the same in VLLM's kernel and Tri Dao's kernel, so we need to parse it
    flash_kwargs[cache.get_block_table_key(flash_attn_with_kvcache)] = block_table[group_idx]
    # Call flash_attn_with_kvcache - this updates cache in-place and computes attention
    attn_output = flash_attn_with_kvcache(
        q=q,
        k_cache=k_cache,
        v_cache=v_cache,
        k=k,
        v=v,
        cache_seqlens=cache_seqlens,
        softmax_scale=module.scaling,
        causal=True,
        window_size=sliding_window,
        **flash_kwargs,
    )
    if isinstance(attn_output, tuple):
        attn_output = attn_output[0]
    # Reshape output from [batch_size, 1, num_heads, head_dim] to [batch_size, num_heads, head_dim]
    return attn_output.squeeze(1)


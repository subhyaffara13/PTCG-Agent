
def sdpa_attention_paged_forward(
    module: torch.nn.Module,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attention_mask: torch.Tensor | None,
    dropout: float = 0.0,
    scaling: float | None = None,
    **kwargs,
) -> tuple[torch.Tensor, None]:
    # Add KV cache to the key and value tensors
    cache: PagedAttentionCache | None = kwargs.pop("cache", None)
    if cache is not None:
        # This changes the shape of k and v from [1, num_kv_heads, seqlen_kv, head_dim] to [-1, num_kv_heads, head_dim]
        key, value = cache.update(
            key_states=key,
            value_states=value,
            layer_idx=module.layer_idx,
            read_index=kwargs["read_index"],
            write_index=kwargs["write_index"],
        )
        key = key.transpose(0, 1).unsqueeze(0)
        value = value.transpose(0, 1).unsqueeze(0)

    # Repeat the key and value tensors for each group of key-value heads
    if hasattr(module, "num_key_value_groups"):
        key = repeat_kv(key, module.num_key_value_groups)
        value = repeat_kv(value, module.num_key_value_groups)

    # Get the right causal mask for the current layer
    causal_mask = attention_mask

    # Run the actual attention
    query = query.contiguous()
    key = key.contiguous()
    value = value.contiguous()
    attn_output = torch.nn.functional.scaled_dot_product_attention(
        query,
        key,
        value,
        attn_mask=causal_mask,
        dropout_p=dropout,
        scale=scaling,
        # Packed sequence format is used for input, so that it can never be causal.
        is_causal=False,
    )
    attn_output = attn_output.transpose(1, 2).contiguous()

    return attn_output, None


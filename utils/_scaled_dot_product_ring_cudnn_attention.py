
def _scaled_dot_product_ring_cudnn_attention(
    mesh: DeviceMesh,
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    attn_bias: torch.Tensor | None = None,
    compute_log_sumexp: bool = True,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    *,
    scale: float | None = None,
) -> tuple[torch.Tensor, ...]:
    if attn_bias is not None:
        raise NotImplementedError("attn_bias is not supported yet")

    if not compute_log_sumexp:
        # CP requires compute_log_sumexp to be True because it always merges LSE
        compute_log_sumexp = True

    # TODO: remove this hardcoding
    seq_dim = 2
    group = mesh.get_group()
    return _templated_ring_attention(
        group,
        seq_dim,
        aten._scaled_dot_product_cudnn_attention,
        query=query,
        key=key,
        value=value,
        attn_bias=attn_bias,
        compute_log_sumexp=compute_log_sumexp,
        dropout_p=dropout_p,
        is_causal=is_causal,
        return_debug_mask=return_debug_mask,
        scale=scale,
    )


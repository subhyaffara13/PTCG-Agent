
def meta__scaled_dot_product_flash_attention_for_cpu(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    attn_mask: Tensor | None = None,
    scale: float | None = None,
):
    batch_size = query.size(0)
    num_heads = query.size(1)
    max_seqlen_batch_q = query.size(2)

    attention = torch.empty_like(query)
    logsumexp = torch.empty(
        (
            batch_size,
            max_seqlen_batch_q,
            num_heads,
        ),
        dtype=torch.float,
        device=query.device,
    ).transpose(1, 2)
    return (
        attention,
        logsumexp,
    )


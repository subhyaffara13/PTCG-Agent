
def meta__scaled_dot_product_flash_attention_quantized(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    q_descale: Tensor | None,
    k_descale: Tensor | None,
    v_descale: Tensor | None,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    scale: float | None = None,
):
    if query.dtype == torch.float8_e4m3fn:
        query = query.to(torch.bfloat16)

    return meta__scaled_dot_product_flash_attention(
        query,
        key,
        value,
        dropout_p,
        is_causal,
        return_debug_mask,
        scale,
    )


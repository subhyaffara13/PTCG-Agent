
def _fa3_scaled_dot_product_flash_attention_forward_impl_default(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    return_debug_mask: bool = False,
    *,
    scale: float | None = None,
):
    return _fa3_scaled_dot_product_flash_attention_forward_impl(
        query,
        key,
        value,
        None,
        None,
        None,
        dropout_p,
        is_causal,
        return_debug_mask,
        scale=scale,
    )


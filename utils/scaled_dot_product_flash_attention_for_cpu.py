
def scaled_dot_product_flash_attention_for_cpu(
    query: Tensor,
    key: Tensor,
    value: Tensor,
    dropout_p: float = 0.0,
    is_causal: bool = False,
    *,
    attn_mask: Tensor | None = None,
    scale: float | None = None,
) -> tuple[Tensor, Tensor]:
    torch._check(
        torch.is_floating_point(query),
        lambda: f"query must be FP32, FP64, BF16, FP16 but got {query.dtype}",
    )
    torch._check(
        query.dim() == 4 and key.dim() == 4 and value.dim() == 4,
        lambda: f"q, k, v must be a 4 dimensional tensor, got {query.dim()}, {key.dim()}, {value.dim()}",
    )
    torch._check(
        dropout_p == 0.0, lambda: f"dropout probability must be zero, got {dropout_p}"
    )
    torch._check(
        query.shape[3] == value.shape[3] and key.shape[3] == value.shape[3],
        lambda: "q, k, v should have the same head size",
    )

    output, attn = aten._scaled_dot_product_attention_math.default(
        query,
        key,
        value,
        attn_mask=attn_mask,
        dropout_p=dropout_p,
        is_causal=is_causal,
        dropout_mask=None,
        scale=scale,
        enable_gqa=query.size(1) != key.size(1),
    )
    # Why this change?
    # In pre-dispatch export scaled_dot_product_attention is executed via
    # * flash_attention.
    # flash_attention allocates output tensor as (N, H, L, E) (see PR #134656)
    # assume x: [N, H, L, E] is the output sdpa
    # In MHA code, this output is then permuted via (2, 0, 1, 3) to get
    # (L, N, H, E) dim tensor
    # x = x.permute(2, 0, 1, 3).contiguous() and the viewed via
    # x = x.view(L * N, H * E)
    # During pre autograd dispatch call to contiguous is not traced because
    # flash_attention output after the x.permute is already contiguous
    # on which the view is valid
    # However, during 2nd stage export, post-dispatch, we run _match variant
    # instead of flash* to get the decomposition. _match variant returns
    # x: [N, H, L, E] applying x.permute(2, 0, 1, 3) returns
    # x: [L, N, H, E] and without converting this to contiguous tensor
    # subsequent view is not valid and the export fails
    # solution is to maintain the return tensor view from the decomp to be
    # exactly same as *flash* variant.

    # Really the invariant you want to maintain is:
    # pre-dispatch op-output and its decomposed representation must
    # return tensor with same view and dims
    output = (
        output.permute(2, 0, 1, 3)
        .contiguous(memory_format=torch.contiguous_format)
        .permute(1, 2, 0, 3)
    )
    return output, attn



def meta__efficient_attention_backward(
    grad_out: Tensor,
    query: Tensor,
    key: Tensor,
    value: Tensor,
    bias: Tensor | None,
    cu_seqlens_q: Tensor | None,
    cu_seqlens_k: Tensor | None,
    max_seqlen_q: torch.SymInt,
    max_seqlen_k: torch.SymInt,
    logsumexp: Tensor,
    dropout_p: float,
    philox_seed: Tensor,
    philox_offset: Tensor,
    custom_mask_type: int,
    bias_requires_grad: bool,
    scale: float | None = None,
    num_splits_key: int | None = None,
    shared_storage_dqdkdv: bool = False,
):
    if shared_storage_dqdkdv:
        torch._check(
            query.shape[1] == key.shape[1],
            lambda: "seqlen must match for `shared_storage_dqdkdv",
        )
        torch._check(
            query.shape[3] == key.shape[3],
            lambda: "embedding dim must match for `shared_storage_dqdkdv",
        )
        chunk = torch.empty(
            (*query.shape[0:-2], 3, query.shape[-2], query.shape[-1]),
            dtype=query.dtype,
            device=query.device,
        )
        grad_query = chunk.select(-3, 0)
        grad_key = chunk.select(-3, 1)
        grad_value = chunk.select(-3, 2)
    else:
        grad_query = torch.empty_like(query)
        grad_key = torch.empty_like(key)
        grad_value = torch.empty_like(value)

    if bias is not None:
        lastDim = bias.size(-1)
        lastDimAligned = lastDim if lastDim % 16 == 0 else lastDim + 16 - lastDim % 16
        new_sizes = list(bias.size())
        new_sizes[-1] = lastDimAligned
        grad_bias = torch.empty(new_sizes, dtype=bias.dtype, device=bias.device)
        grad_bias = grad_bias[..., :lastDim]
    else:
        grad_bias = torch.empty((), device=query.device)

    return grad_query, grad_key, grad_value, grad_bias


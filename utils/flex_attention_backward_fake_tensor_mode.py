
def flex_attention_backward_fake_tensor_mode(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    grad_out: torch.Tensor,
    grad_logsumexp: torch.Tensor,
    fw_graph: Callable | GraphModule,
    joint_graph: GraphModule,
    block_mask: tuple,
    scale: float,
    kernel_options: dict[str, Any],
    score_mod_other_buffers: tuple = (),
    mask_mod_other_buffers: tuple = (),
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, tuple[torch.Tensor | None, ...]]:
    if has_user_subclass(
        (
            query,
            key,
            value,
            out,
            logsumexp,
            grad_out,
            grad_logsumexp,
            block_mask,
            scale,
            kernel_options,
            score_mod_other_buffers,
            mask_mod_other_buffers,
        ),
        allowed_subclasses=(FakeTensor,),
    ):
        return NotImplemented
    Bq, _, _, qk_head_dim = query.shape
    Bkv, Hkv, seq_len_kv, v_head_dim = value.shape

    grad_query = query.new_empty(query.shape)
    grad_query = _permute_strides(grad_query, query.stride())
    # zeros_and_scatter creates a contiguous zeros tensor -> contiguous_format
    grad_score_mod_captured = tuple(
        (
            torch.empty_like(buffer, memory_format=torch.contiguous_format)
            if isinstance(buffer, torch.Tensor)
            else None
        )
        for buffer in score_mod_other_buffers
    )

    broadcasted_grad_key = key.new_empty((Bq, Hkv, seq_len_kv, qk_head_dim))
    broadcasted_grad_key = _permute_strides(broadcasted_grad_key, key.stride())

    broadcasted_grad_value = value.new_empty((Bq, Hkv, seq_len_kv, v_head_dim))
    broadcasted_grad_value = _permute_strides(broadcasted_grad_value, value.stride())

    if Bq > 1 and Bkv == 1:
        grad_key = torch.sum(broadcasted_grad_key, dim=0, keepdim=True)
        grad_value = torch.sum(broadcasted_grad_value, dim=0, keepdim=True)
    else:
        grad_key = broadcasted_grad_key
        grad_value = broadcasted_grad_value

    return grad_query, grad_key, grad_value, grad_score_mod_captured

